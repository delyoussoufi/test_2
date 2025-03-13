from dataclasses import dataclass, asdict

from flaskapp.structures import Cast


@dataclass
class BaseDataClass:

    @classmethod
    def from_dict(cls, dto: dict):
        return Cast(dto, cls)

    def to_dict(self):
        return asdict(self)
