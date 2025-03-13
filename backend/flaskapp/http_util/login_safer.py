import datetime as dt
from dataclasses import dataclass
from functools import wraps
from typing import Dict, Callable

from flask import request


@dataclass
class UserLoginLog:
    username: str
    last_login_time: dt.datetime = dt.datetime.now()
    total_attempts: int = 0
    fail_attempts: int = 0


class SafeLogin:

    _BLOCK_USERS: Dict[str, dt.datetime] = {}
    _LOGIN_LOG: Dict[str, UserLoginLog] = {}

    def __init__(self, username, block_user_after_x_attempts=5):
        self._username = username
        self.block_user_after_x_attempts = block_user_after_x_attempts
        self.error_on_block = PermissionError
        self.__user_log = self._LOGIN_LOG.get(self._username, UserLoginLog(username=self._username))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_user_log()

    @property
    def blocked_time(self):
        blocked_until = self._BLOCK_USERS.get(self._username, dt.datetime.now())
        blocked_time = (blocked_until - dt.datetime.now()).seconds
        return max(0, blocked_time)

    @property
    def user_log(self):
        return self.__user_log

    def save_user_log(self):
        self._LOGIN_LOG[self._username] = self.user_log

    def add_attempts(self):

        self.user_log.total_attempts += 1
        self.save_user_log()

    def add_fail_attempts(self):

        self.user_log.fail_attempts += 1
        self.save_user_log()

        if self.user_log.fail_attempts >= self.block_user_after_x_attempts:
            # block user for x minutes, where x increases with fail attempts
            self.block_user(time=60*self.user_log.fail_attempts)

    def block_user(self, time: int):
        """
        Block user from logging for x seconds.

        :param time: Time to block in seconds.
        :return:
        """
        block_until = dt.datetime.now() + dt.timedelta(seconds=time)
        self._BLOCK_USERS[self._username] = block_until

    def is_blocked(self):

        block_time = self._BLOCK_USERS.get(self._username, None)

        if not block_time:
            # user has no block time. Not a blocked user
            return False
        elif block_time > dt.datetime.now():
            # user has a valid block time. Therefore, user is still blocked.
            return True
        else:
            # user has an invalid block time, clean it from block list.
            self.unblock_user()
            return False

    def clean_fail_attempts(self):
        self.user_log.fail_attempts = 0

    def unblock_user(self):
        if self._username in self._BLOCK_USERS.keys():
            self._BLOCK_USERS.pop(self._username)

    def safe_login(self, login_func: Callable, *args, **kwargs):
        self.add_attempts()
        self.user_log.last_login_time = dt.datetime.now()
        if self.is_blocked():
            raise self.error_on_block(f"User {self._username} is blocked for {self.blocked_time} seconds.")
        result = login_func(*args, **kwargs)
        if type(result) == tuple:
            result = result[0]
        if result:
            # if logging function return a values than clean fail attempts and return the value
            self.clean_fail_attempts()
            return result
        else:
            # otherwise, add a fail attempt and return.
            self.add_fail_attempts()
            return result


def safe_login(map_username: str = "username", error_on_block=PermissionError, from_request=True):
    """
    Block users who tries too many attempts of wrong logging, increasing logging safety.

    :param map_username: The expected username field from request or the decorated method.
    :param error_on_block: The error to raise when user is blocked.
    :param from_request: True if username should be get from request form, otherwise try to get from the
        decorated method.
    :return:
    """
    def app_decorator(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            if from_request:
                # if from request try to get username field from there
                username = request.form.get(map_username, None)
            else:
                # otherwise it expects the decorated function to pass it as a kwargs
                username = kwargs.get(map_username, None)
            if not username:
                raise AttributeError(f"The method {func.__name__} must have {map_username} as attribute.")
            with SafeLogin(username) as sl:
                sl.error_on_block = error_on_block
                return sl.safe_login(func, *args, **kwargs)
        return wrap_func
    return app_decorator


if __name__ == '__main__':

    @safe_login(from_request=False)
    def test_login(username, psw):
        if psw == '12':
            return True
        else:
            return False
    try:
        for i in range(20):
            if test_login(username='admin', psw=f'{i}'):
                break
            if test_login(username='admin2', psw=f'{i}'):
                break
            print(f"Trying logging {i+1}")

    except PermissionError:
        print("blocked")

    print(SafeLogin('admin').user_log)
    print(SafeLogin('admin2').user_log)

