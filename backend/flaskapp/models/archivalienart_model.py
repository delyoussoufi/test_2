from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class ArchivalienartModel(db.Model, BaseModel):
    __tablename__ = TableNames.T_ARCHIVALIEN_ARTEN
    id = db.Column(db.String(50), primary_key=True)
    scope_entrg_typ_id = db.Column(db.String(20))
    name = db.Column(db.String(200))

    def to_dict(self):
        dict = {"id": self.id, "scopeEintragTypId": self.scope_entrg_typ_id, "name": self.name}
        return dict

    @classmethod
    def from_dict(cls, dto: dict):
        archivalien_art = ArchivalienartModel()
        archivalien_art.id = dto.get("id", None)
        archivalien_art.scope_entrg_typ_id = dto["scopeEintragTypId"]
        archivalien_art.name = dto["name"]
        return archivalien_art

    @classmethod
    def find_archivalienart_by_scope_eintrag_typ_id(cls, scope_entrg_typ_id: str):
        """
        This will find all archivalienart objects with the scope_entrg_typ_id.

        :param scope_entrg_typ_id: The id of the scope classification.
        :return: A list of DigitalisatModel or None.
        """
        return cls.find_by(scope_entrg_typ_id=scope_entrg_typ_id)