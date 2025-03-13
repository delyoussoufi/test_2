from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import TypeVar, Generic

from sqlalchemy import Column, func

from flaskapp.structures import BaseDataClass
from flaskapp.utils import parse_to_ts_query_string


class QueryOperators(Enum):
    INCLUDE = "CONTAINS", lambda col, val: col.like(f"%{val}%")
    EQUAL = "EQUAL", lambda col, val: col.__eq__(f"{val}")
    BEGINS_WITH = "BEGINSWITH", lambda col, val: col.like(f"{val}%")
    EQUAL_ALIAS = "==", lambda col, val: col.__eq__(f"{val}")
    INCLUDE_ALIAS = "[]", lambda col, val: col.like(f"%{val}%")
    BEGINS_WITH_ALIAS = "]", lambda col, val: col.like(f"{val}%")
    BIGGER = ">", lambda col, val: col.__gt__(f"{val}")
    BIGGER_EQUAL = ">=", lambda col, val: col.__ge__(f"{val}")
    SMALLER = "<", lambda col, val: col.__lt__(f"{val}")
    SMALLER_EQUAL = "<=", lambda col, val: col.__le__(f"{val}")
    NOT_EQUAL = "!=", lambda col, val: col.__ne__(f"{val}")
    LOWER_INCLUDES = "lower_CONTAINS", lambda col, val: col.ilike(f"%{val}%")
    LOWER_INCLUDES_ALIAS = "lower[]", lambda col, val: col.ilike(f"%{val}%")
    LOWER_BEGINS_WITH = "lower_BEGINSWITH", lambda col, val: col.ilike(f"{val}%")
    LOWER_EQUAL = "lower_EQUAL", lambda col, val: func.lower(col).__eq__(f"{val}")
    FULLTEXT = "@@", lambda col, val: col.match(f"{parse_to_ts_query_string(val)}:*", postgresql_regconfig="german")
    FULLTEXT_SIMPLE = "S@@", lambda col, val: col.match(f"{parse_to_ts_query_string(val)}:*",
                                                        postgresql_regconfig="simple")

    def __new__(cls, value, apply_filter=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.apply_filter = apply_filter
        return obj


@dataclass
class ColumnOperator:
    Column: Column
    QueryOp: QueryOperators


@dataclass
class SearchDefault(BaseDataClass):
    """
    Class that holds a structure to perform search and paginate it. This structure can
    be used by any :class:`BaseModel`, since SearchBy and OrderBy are valid column names.
    Use the method from_dict to create an instance from a dictionary.

    Fields:
        SearchBy: A table's column's name to search. You can pass multiple values by using comma separation,
        e.g:
            "username, name".
        This will perform a search in this to columns. SearchBy can also override
        the operator, e.g:
            "username: ==, name: !="

        Valid operator: "==, <,>,<=,>=,!=,[],]"

        SearchValue: The value to search. You can pass multiple values by using comma separation or a List, e.g:
            "John, Sara" or [ "John, Sara"]. This are safer than just comma separation.
        This will perform a search for this values for the given columns.

        Page: The current page to return.

        PerPage: Number of items per page.

        OrderBy: A table's column's name to order.

        OrderDesc: True if the order must be descendant.

        MapColumnAndValue (default = True): If True it will consider a 1:1 mapping for SearchBy:SearchValue.
            e.g: Column -> "username, name", Values -> "admin, Sara".

            If True: This will search for username = like(%admin%) and name = like(%Sara%).

            If False: This will search for username = like(%admin%, %Sara%) and name = like(%admin%, %Sara%).

        Use_AND_Operator (default = False): Makes the search with AND instead of OR.

        TextualQuery: Use a textual query, i.e: "id<1111"

        Join: Used to join query. This must be a tuple where the first element must be a child class
            of BaseModel and the second element must be an object from Search, i.e (UserModel, search)

        Operator (default =  QueryOperators.INCLUDE): A valid QueryOperator. This is used to apply a
            given operator in filter.
    """

    SearchBy: str = " "
    SearchValue: list = field(default_factory=list)
    Page: int = 1
    PerPage: int = 1000
    OrderBy: str = ""
    OrderDesc: bool = False
    MapColumnAndValue: bool = True
    Use_AND_Operator: bool = False
    TextualQuery: str = None
    Join: tuple = None
    Operator: QueryOperators = QueryOperators.INCLUDE

    @property
    def per_page(self):
        return self.PerPage

    @property
    def page(self):
        return self.Page


@dataclass
class Search(BaseDataClass):
    """
    Class that holds a structure to perform search and paginate it. This structure can
    be used by any :class:`BaseModel`, since SearchBy and OrderBy are valid column names.
    Use the method from_dict to create an instance from a dictionary.

    Fields:
        SearchBy: A table's column's name to search. You can pass multiple values by using comma separation,
        e.g:
            "username, name".
        This will perform a search in this to columns. SearchBy can also override
        the operator, e.g:
            "username: ==, name: !="

        Valid operator: "==, <,>,<=,>=,!=,[],]"

        SearchValue: The value to search. You can pass multiple values by using comma separation or a List, e.g:
            "John, Sara" or [ "John, Sara"]. This are safer than just comma separation.
        This will perform a search for this values for the given columns.

        Page: The current page to return.

        PerPage: Number of items per page.

        OrderBy: A table's column's name to order.

        OrderDesc: True if the order must be descendant.

        MapColumnAndValue (default = True): If True it will consider a 1:1 mapping for SearchBy:SearchValue.
            e.g: Column -> "username, name", Values -> "admin, Sara".

            If True: This will search for username = like(%admin%) and name = like(%Sara%).

            If False: This will search for username = like(%admin%, %Sara%) and name = like(%admin%, %Sara%).

        Use_AND_Operator (default = False): Makes the search with AND instead of OR.

        TextualQuery: Use a textual query, i.e: "id<1111"

        Join: Used to join query. This must be a tuple where the first element must be a child class
            of BaseModel and the second element must be an object from Search, i.e (UserModel, search)

        Operator (default =  QueryOperators.INCLUDE): A valid QueryOperator. This is used to apply a
            given operator in filter.
    """

    SearchBy: str
    SearchValue: list
    Page: int
    PerPage: int
    OrderBy: str
    OrderDesc: bool = False
    MapColumnAndValue: bool = True
    Use_AND_Operator: bool = False
    TextualQuery: str = None
    Join: tuple = None
    Operator: QueryOperators = QueryOperators.INCLUDE


T = TypeVar('T')


@dataclass
class SearchResult(Generic[T], BaseDataClass):
    """
    Class that holds a structure to return a search result.

    Fields:
        result: Expect a list of entities. However, it can be any object list that implements the method to_dict().

        total: The total number of entities found.
    """

    resultList: list[T] = field(default_factory=list)
    totalCount: int = 0

    def to_dict(self) -> dict:
        """
        Map this object to a dictionary.

        :return: The dictionary representation of this object.
        """
        search_result_asdict = asdict(self)
        search_result_asdict["resultList"] = [entity.to_dict() for entity in self.resultList]
        return search_result_asdict


@dataclass
class SystemDiskInfo(BaseDataClass):
    """
    Class that holds a structure to return the file info of the pre upload dir.

    Fields:
        totalDiskSpace: Total disk space.

        usedDiskSpace: Used disk space.

        availableDiskSpace: Available disk space.
    """

    totalDiskSpace: float
    usedDiskSpace: float
    availableDiskSpace: float


@dataclass
class DigitalisateInfo(BaseDataClass):
    """
    Class that holds a structure to return the digitalisate info.

    Fields:
        status: The status of digitalisate.

        total: The number of digitalisate with this status.
    """

    status: str
    total: int
