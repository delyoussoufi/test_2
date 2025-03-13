from datetime import datetime

from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class UserRightModel(db.Model, BaseModel):

    # The name of the table at the database.
    __tablename__ = TableNames.T_USER_RIGHTS

    # The table columns.
    user_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_USER + ".user_id"), primary_key=True)
    right_id = db.Column(db.String(50), db.ForeignKey(TableNames.S_RIGHTS + ".right_id"), primary_key=True)
    lastchange_by = db.Column(db.String(16), unique=False, nullable=True)
    lastchange_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return BaseModel.__repr__(self)
