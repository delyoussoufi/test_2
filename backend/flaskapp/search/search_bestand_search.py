from dataclasses import dataclass

from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import Search, QueryOperators


@dataclass
class SearchBestandSearch(BaseDataClass):
    """
    Class that holds a structure to perform a join search for bestand and paginate it.
    """
    name: str = ""
    operator: str = QueryOperators.INCLUDE.value
    orderBy: str = "name"
    orderDirection: str = None
    firstResult: int = 1
    maxResults: int = 1000

    @property
    def page(self):
        return round(self.firstResult / self.maxResults) + 1

    @property
    def per_page(self):
        return self.maxResults

    def to_search(self):
        search_by = "name"
        search_value = f"{self.name}"
        return Search(SearchBy=search_by, SearchValue=[search_value], Use_AND_Operator=True, OrderBy=self.orderBy,
                      OrderDesc=self.orderDirection == "DESC", Page=self.page, PerPage=self.per_page,
                      Operator=QueryOperators(self.operator))
