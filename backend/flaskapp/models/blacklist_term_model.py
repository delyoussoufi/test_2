from flaskapp import db
from flaskapp.models import TableNames, BaseModel


class BlacklistTermModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_BLACKLIST_TERM
    id = db.Column(db.String(16), primary_key=True)
    category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"))
    value = db.Column(db.String(255))

    def to_dict(self):
        dto = super().to_dict()
        dto.setdefault("categoryId", dto.pop("category_id", None))
        return dto

    @classmethod
    def from_dict(cls, dto: dict):
        model: cls = super().from_dict(dto)
        model.category_id = dto.get("categoryId", None)
        return model
