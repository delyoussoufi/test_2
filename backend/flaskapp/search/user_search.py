from dataclasses import dataclass

from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import Search, QueryOperators


@dataclass
class UserSearch(BaseDataClass):
    """
    Class that holds a structure to perform a search for user and paginate it.

    Fields:
        * username = (string) the username of the user.

        * forename = (string) forename of the user.

        * surname = (string) surname of the user.
    """

    username: str = ""
    forename: str = ""
    surname: str = ""
    operator: str = None
    orderBy: str = "username"
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
        searchBy = "username"
        searchValue = [f'{self.username}']
        if self.forename:
            searchBy += ",forename"
            searchValue += f",{self.forename}"
        if self.surname:
            searchBy += ",surname"
            searchValue += f",{self.surname}"
        return Search(SearchBy=searchBy, SearchValue=searchValue, Use_AND_Operator=True, OrderBy=self.orderBy,
                      OrderDesc=self.orderDirection == "ASC", Page=self.page, PerPage=self.per_page,
                      TextualQuery="", Operator=QueryOperators(self.operator))
