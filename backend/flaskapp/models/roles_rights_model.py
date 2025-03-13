from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class RolesRightsModel(db.Model, BaseModel):

    # The name of the table at the database.
    __tablename__ = TableNames.T_ROLES_RIGHTS

    # The table columns.
    role_id = db.Column(db.String(16), db.ForeignKey(TableNames.S_ROLES + ".user_id"), primary_key=True)
    right_id = db.Column(db.String(50), db.ForeignKey(TableNames.S_RIGHTS + ".right_id"), primary_key=True)

    def __repr__(self):
        return BaseModel.__repr__(self)
