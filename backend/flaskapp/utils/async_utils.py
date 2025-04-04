import time
from functools import wraps
from threading import Thread
from typing import Callable


class AsyncTime(Thread):

    def __init__(self):
        super().__init__()
        self.seconds = 1
        self.__callback = None
        self.__return_callback = None
        self.__obj = None

    def run(self) -> None:
        if self.seconds != 0:
            time.sleep(self.seconds)
        result = None
        if self.__callback:
            result = self.__callback()
        if self.__return_callback:
            self.__return_callback(self.__obj, result)

    def set_return_callback(self, obj, func):
        """
        Set a method to get the return value of this process. The method must have a result argument.
        :param obj: The self object for this method.
        :param func: A method to catch the return value of the running method.
        :return:
        """
        self.__return_callback = func
        self.__obj = obj

    def wait(self, seconds: float, func: Callable):
        """
        Wait x seconds in a different thread.
        :param seconds: Time in seconds to wait.
        :param func: The callback function. This will be called when the waiting time is over.
        :return:
        """
        self.seconds = seconds
        self.__callback = func
        self.start()

    @staticmethod
    def async_wait(seconds: float):
        """
         Wait x seconds in a different thread before execute the decorated method.
        :param seconds: seconds: Time in seconds to wait.
        :return:
        """
        def app_decorator(func):
            @wraps(func)
            def wrap_func(*args, **kwargs):
                AsyncTime().wait(seconds, lambda: func(*args, **kwargs))
            return wrap_func
        return app_decorator

    @staticmethod
    def run_async(return_value_callback=None):
        """
         Runs a method in a different thread.
        :return:
        """

        def app_decorator(func):
            @wraps(func)
            def wrap_func(*args, **kwargs):
                new_thread = AsyncTime()
                new_thread.set_return_callback(args[0], return_value_callback)
                new_thread.wait(0, lambda: func(*args, **kwargs))
            return wrap_func
        return app_decorator
