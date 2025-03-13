from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class RightModel(db.Model, BaseModel):

    # The name of the table at the database.
    __tablename__ = TableNames.S_RIGHTS

    # The table columns.
    right_id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return BaseModel.__repr__(self)
