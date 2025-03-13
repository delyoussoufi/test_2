from dataclasses import dataclass

from flaskapp.structures import BaseDataClass


@dataclass
class DigiBestandSearch(BaseDataClass):
    """
    Class that holds a structure to perform a join search for bestand and paginate it.

    Fields:
        * name = (string) the name of the bestand.

        * signature = (string) signatur in the bestand.

        * scopeId = (string) scopeId in the bestand.
    """

    name: str = ""
    signature: str = ""
    scopeId: str = ""
    operator: str = None
    orderBy: str = ""
    orderDirection: str = None
    firstResult: int = 1
    maxResults: int = 1000

    @property
    def page(self):
        return round(self.firstResult / self.maxResults) + 1

    @property
    def per_page(self):
        return self.maxResults
