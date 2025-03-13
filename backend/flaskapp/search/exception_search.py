from dataclasses import dataclass

from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import Search
from flaskapp.utils import DateUtils


@dataclass
class ExceptionSearch(BaseDataClass):
    """
    Class that holds a structure to perform a search for exception and paginate it.

    Fields:
        * name = (string) the name of the bestand.

        * signatur = (string) signatur in the bestand.

        * scopeId = (string) scopeId in the bestand.
    """

    stacktrace: str = ""
    hash: int = None
    dateVon: str = None
    dateBis: str = None
    selectedPeriod: str = None
    orderBy: str = "date"
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
        search_by = "stacktrace"
        search_values = [f'{self.stacktrace}']
        text_query = ""
        text_queries = []
        if self.hash:
            text_queries.append(f'hash={self.hash}')
        if self.dateVon:
            date_str = DateUtils.convert_german_string_to_date(self.dateVon)
            text_queries.append(f"date>='{date_str}'")
        if self.dateBis:
            date_str = DateUtils.convert_german_string_to_date(self.dateBis)
            text_queries.append(f"date<='{date_str}'")
        for i, query_part in enumerate(text_queries):
            if i == 0:
                text_query += query_part
            else:
                text_query += " AND " + query_part
        return Search(SearchBy=search_by, SearchValue=search_values, Use_AND_Operator=True, OrderBy=self.orderBy,
                      OrderDesc=self.orderDirection == "DESC", Page=self.page, PerPage=self.per_page,
                      TextualQuery=text_query)
