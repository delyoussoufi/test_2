from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class RoleModel(db.Model, BaseModel):

    # The name of the table at the database.
    __tablename__ = TableNames.S_ROLES

    # The table columns.
    role_id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "Role(role_id={})".format(self.role_id)

    @classmethod
    def is_valid_role(cls, role_id: str):
        role = cls.find_by_id(role_id)
        if role:
            return True
        return False

    def to_dict(self):
        """
        Convert RoleModel into a dictionary, this way we can convert it to a JSON response.

        :return: A clean dictionary form of this model.
        """
        # convert columns to dict
        dict_representation = super().to_dict()
        dict_representation["authority"] = self.role_id
        return dict_representation


