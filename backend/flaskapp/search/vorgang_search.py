from dataclasses import dataclass

from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import Search, QueryOperators
from flaskapp.utils import DateUtils


@dataclass
class VorgangSearch(BaseDataClass):
    """
    Class that holds a structure to perform a join search for vorgang and paginate it.
    """
    vorgangsnummer: str = ""
    createDateBegin: str = ""
    createDateEnd: str = ""
    searchCategoryId: str = ""
    operator: str = QueryOperators.INCLUDE.value
    orderBy: str = "create_date"
    orderDirection: str = None
    page: int = 1
    perPage: int = 1000

    def to_search(self):
        search_by = "search_category_id"
        search_value = [f"{self.searchCategoryId}"]
        if self.createDateBegin:
            search_by += ",create_date:>="
            search_value += f",{DateUtils.convert_german_string_to_date(self.createDateBegin)}"
        if self.createDateEnd:
            search_by += ",create_date:<="
            search_value += f",{DateUtils.convert_german_string_to_date(self.createDateEnd)}"
        return Search(SearchBy=search_by, SearchValue=search_value, Use_AND_Operator=True, OrderBy=self.orderBy,
                      OrderDesc=self.orderDirection == "DESC", Page=self.page, PerPage=self.perPage,
                      Operator=QueryOperators(self.operator))
