from dataclasses import dataclass, field, asdict
from typing import List, Union


@dataclass
class Box:
    x0: float
    y0: float
    xf: float
    yf: float

    def __mul__(self, scalar: Union[int, float]):
        return Box(x0=self.x0 * scalar, y0=self.y0 * scalar, xf=self.xf * scalar, yf=self.yf * scalar)


@dataclass
class Word:
    box: Box
    confidence: float = field(default=0.)
    text: str = field(default="")


@dataclass
class OcrData:
    words: List[Word] = field(default_factory=list)
    text: str = field(default="")

    def to_dict(self):
        return asdict(self)
