from datetime import date, timedelta, datetime, time
from dateutil import parser
from typing import Tuple, Union


class DateUtils:
    TIME_PATTERN = "HH:mm"

    @staticmethod
    def is_date(date_string: str) -> bool:
        try:
            parser.parse(date_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_system_date(date_str: str) -> Union[date, None]:
        """
        Convert a string to a date type.
        :param date_str: The date format string to be converted.
        :return: The date.
        """
        if date_str:
            return parser.parse(date_str).date()
        return None

    @staticmethod
    def parse_system_time(date_str: str) -> Union[time, None]:
        """
        Convert a string to a date/time type.
        :param date_str: The date format string to be converted.
        :return: The date.
        """
        if date_str:
            return parser.parse(date_str).time()
        return None

    @staticmethod
    def parse_system_date_time(date_str: str) -> Union[datetime, None]:
        """
        Convert a string to a date time type.
        :param date_str: The date format string to be converted.
        :return: The date time.
        """
        if date_str:
            return parser.parse(date_str, ignoretz=True)
        return None

    @staticmethod
    def convert_german_string_to_date(date_str: str) -> Union[date, None]:
        """
        Convert a string to a date type.
        :param date_str: The date format string to be converted.
        :return: The date.
        """
        if date_str:
            return parser.parse(date_str, dayfirst=True).date()
        return None

    @staticmethod
    def convert_date_to_german_string(_date: Union[date, datetime], add_time=False) -> str or None:
        """
        Creates a german date string from the date. The date string is a string of dd.mm.YYYY
        :param _date: The date
        :param add_time: If True time is added to date format
        :return: A string like dd.mm.YYYY or dd.mm.YYYY H:M:S
        """
        if _date:
            if add_time:
                return _date.strftime('%d.%m.%Y %H:%M:%S')
            return _date.strftime('%d.%m.%Y')
        return None

    @staticmethod
    def convert_date_time_to_time_string(_date: datetime) -> str or None:
        """
        Creates a time string from the date. The time string is a string of dd.mm.YYYY
        :param _date: The date
        :return: A string like dd.mm.YYYY
        """
        if _date:
            return _date.strftime('%H:%M')
        return None

    @staticmethod
    def parse_time(time_str: str) -> date:
        parsed_date = parser.parse(time_str)
        return parsed_date

    @staticmethod
    def add_days(_date: date or datetime, days: int) -> date:
        return _date + timedelta(days=days)

    @staticmethod
    def days_between_dates(start: date, end: date) -> int:
        delta = end - start
        return delta.days

    @classmethod
    def create_timestamp(cls):
        """
        Gets the current datetime in the format of dd.mm.YYYY HH:MM:SS
        :return: A string of datetime format: dd.mm.YYYY HH:MM:SS
        """
        return datetime.now().__format__("%d.%m.%Y %H:%M:%S")
