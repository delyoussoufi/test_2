import re
from functools import wraps


class MapAttributes(object):

    @staticmethod
    def map_to_ts_style(value: str) -> str:
        if not value:
            return value

        values: list[str] = value.split('_')
        if len(values) == 1:
            return values[0]

        first_value = values.pop(0)  # remove first item of the list. Don't want to capitalize.
        capitalize_values = "".join([parts.capitalize() for parts in values])
        return f"{first_value}{capitalize_values}"

    @classmethod
    def map_to_py_style(cls, value: str) -> str:
        return "_".join(re.split(r"(?=[A-Z])", value)).lower()


def map_to_ts_style():
    """

    :return:
    """

    def app_decorator(func_):
        @wraps(func_)
        def wrap_func(*args, **kwargs) -> dict:
            dto: dict = func_(*args, **kwargs)
            if not isinstance(dto, dict):
                raise AttributeError(f"The return value of a {func_} is not a dict")

            return {MapAttributes.map_to_ts_style(key): value for key, value in dto.items()}

        return wrap_func

    return app_decorator


def map_to_py_style():
    """

    :return:
    """

    def app_decorator(func_):
        @wraps(func_)
        def wrap_func(*args, **kwargs) -> dict:

            def mapper(v_: any):
                if isinstance(v_, dict):
                    return {MapAttributes.map_to_py_style(key): value for key, value in v_.items()}
                else:
                    return v_

            kwargs = {k: mapper(v) for k, v in kwargs.items()}
            args = tuple(mapper(v) for v in args)

            return func_(*args, **kwargs)

        return wrap_func

    return app_decorator
