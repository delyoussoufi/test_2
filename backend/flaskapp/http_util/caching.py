import inspect
from functools import wraps
from typing import Callable, Union

from flaskapp import cache

DEFAULT_CACHE_TIME = 10*24*3600  # time in seconds the cache will last.


def validate_class_function(func: Callable):

    if not any(k in ["cls", "self"] for k in inspect.signature(func).parameters.keys()):
        raise AttributeError(f"The method {func.__name__} doesn't implement self or cls attribute.")


def is_class_function(func: Callable):
    sig = inspect.signature(func)
    if sig.parameters.get('self', None) or sig.parameters.get('cls', None):
        return True
    else:
        return False


def cacheable(value: str = "", timeout=DEFAULT_CACHE_TIME, unless=None):
    """

    :param value: If a value is passed it will use cache.cached, otherwise
        it uses cache.memoize. The value is passed to key_prefix parameter in cache.cached.
        Only use this if you have no arguments in your method, otherwise this will cache
        the same result for different passed arguments.

    :param timeout:  Default None. If set to an integer, will cache for that amount of time. Unit of time is in seconds.

    :param unless: Default None. Cache will *always* execute the caching facilities unless
        this callable is true. This will bypass the caching entirely.
    :return:
    """

    def app_decorator(func):
        if value and is_class_function(func):
            raise AttributeError(f"Illegal operation don't pass cache value to a class method.")

        if value:
            func = cache.cached(timeout=timeout, key_prefix=value, unless=unless)(func)
        else:
            func = cache.memoize(timeout=timeout, unless=unless)(func)

        @wraps(func)
        def wrap_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrap_func
    return app_decorator


def delete_cache(value: Union[str, Callable], delete_all: bool = False):
    """

    :param value:
    :param delete_all:
    :return:
    """
    def app_decorator(func):

        @wraps(func)
        def wrap_func(*args, **kwargs):
            if callable(value):
                f = value
            elif is_class_function(func):
                # try to get method from the first args, expected to be self or cls.
                f = getattr(args[0], value)
            else:
                f = value
            try:
                if delete_all:
                    cache.delete_memoized(f)
                else:
                    cache.delete_memoized(f, *args, **kwargs)
            except TypeError:
                cache.delete(value)

            return func(*args, **kwargs)

        return wrap_func
    return app_decorator
