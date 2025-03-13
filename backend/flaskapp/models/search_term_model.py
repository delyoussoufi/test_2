from flaskapp import db
from flaskapp.http_util.mapper import map_to_ts_style, map_to_py_style
from flaskapp.models import TableNames, BaseModel


class SearchTermModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_SEARCH_TERM
    id = db.Column(db.String(16), primary_key=True)
    category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"))
    search_value = db.Column(db.String(255))

    @map_to_ts_style()
    def to_dict(self):
        """
        Convert SearchTermModel into a dictionary, this way we can convert it to a JSON response.

        :return: A clean dictionary form of this model.
        """
        return super().to_dict()

    @classmethod
    @map_to_py_style()
    def from_dict(cls, dto: dict) -> 'SearchTermModel':
        # noinspection PyTypeChecker
        return super().from_dict(dto)
