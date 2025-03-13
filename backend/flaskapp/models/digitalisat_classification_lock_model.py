from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class DigitalisatClassificationLockModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_DIGITALISAT_CLASSIFICATION_LOCK

    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"), primary_key=True)
    search_category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"), primary_key=True)

    def __repr__(self):
        BaseModel.__repr__(self)

    @classmethod
    def is_locked(cls, digitalisat_id: str, search_category_id: str):
        model = cls.find_by_id(digitalisat_id, search_category_id)
        if model:
            return True
        return False
