from dataclasses import dataclass, field, asdict
from typing import List


# TODO Not sure if you are using this??
@dataclass
class Words:
    index: int
    word: str


@dataclass
class Box:
    x0: float
    y0: float
    xf: float
    yf: float


@dataclass
class FoundTerm:
    box: Box
    value: str
    score: float
    score_unit: str


@dataclass
class SearchTerm:
    value: str
    found_terms: List[FoundTerm] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
