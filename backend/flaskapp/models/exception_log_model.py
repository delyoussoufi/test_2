from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class ExceptionLogModel(db.Model, BaseModel):
    __tablename__ = TableNames.T_EXCEPTION_LOG

    id = db.Column(db.String(16), primary_key=True)
    hash = db.Column(db.Integer)
    title = db.Column(db.String(255))
    stacktrace = db.Column(db.String(5000))
    date = db.Column(db.DateTime)
