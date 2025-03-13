from dataclasses import dataclass

from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import Search, QueryOperators


@dataclass
class SearchCategorySearch(BaseDataClass):
    """
    Class that holds a structure to perform a join search for bestand and paginate it.
    """
    name: str = ""
    description: str = ""
    operator: str = QueryOperators.INCLUDE.value
    orderBy: str = "name"
    orderDesc: bool = False
    page: int = 1
    perPage: int = 1000

    @property
    def per_page(self):
        return self.perPage

    def to_search(self):
        search_by = "name"
        search_value = [f"{self.name}"]
        if self.description:
            search_by += ",description"
            search_value += f",{self.description}"
        return Search(SearchBy=search_by, SearchValue=search_value, Use_AND_Operator=True, OrderBy=self.orderBy,
                      OrderDesc=self.orderDesc, Page=self.page, PerPage=self.per_page,
                      Operator=QueryOperators(self.operator))
