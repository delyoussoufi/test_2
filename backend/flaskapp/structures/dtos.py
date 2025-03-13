from dataclasses import dataclass

from flaskapp.http_util.mapper import map_to_py_style, map_to_ts_style
from flaskapp.models import UserModel, TokenModel
from flaskapp.structures import BaseDataClass


@dataclass
class ProfileDto(BaseDataClass):
    user_id: str
    username: str
    surname: str = ''
    forename: str = ''
    password: str = None
    repeated_password: str = None

    @classmethod
    @map_to_py_style()
    def from_dict(cls, dto: dict):
        return super().from_dict(dto=dto)

    @map_to_ts_style()
    def to_dict(self):
        return super().to_dict()
