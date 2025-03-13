from dataclasses import dataclass, field

from flaskapp.models.enums import DigitalisatStatus
from flaskapp.structures import BaseDataClass
from flaskapp.structures.structures import SearchDefault


@dataclass
class ScopeMetadataSearch(BaseDataClass):
    title: str = ""
    geburtsname: str = ""
    wohnort: str = ""
    registrySignature: str = ""
    associates: str = ""
    laufzeit: str = ""
    startSignature: int = 0
    endSignature: int = 0
    comments: str = ""

    def is_empty(self):
        # returns True if there is no values in ScopeMetadataSearch
        return all([not bool(v) for v in self.to_dict().values() if v])


@dataclass
class DigitalisatSearch(SearchDefault):
    """
    Class that holds a structure to perform a join search for digitalisat and paginate it.
    """
    classificationStatusId: str = ""
    status: str = DigitalisatStatus.FINISHED.name
    classificationStatus: str = ""  # Should be on of the values from Enum ClassificationStatus
    textSearch: str = ""
    metadata: ScopeMetadataSearch = field(default_factory=ScopeMetadataSearch)
