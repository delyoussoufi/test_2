from typing import List

from flask_login import UserMixin

from flaskapp import db, login_manager, app_logger, app_utils
from flaskapp.http_util import exceptions
from flaskapp.http_util.mapper import map_to_py_style, map_to_ts_style
from flaskapp.models import Relationship, TableNames, UserRoleModel, RoleModel, TokenModel, UserRightModel
from flaskapp.models.base_model import BaseModel


class UserModel(db.Model, BaseModel, UserMixin):

    # The name of the table at the database.
    __tablename__ = TableNames.T_USER

    # The table columns.
    user_id = db.Column(db.String(16), primary_key=True)
    forename = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)

    roles = db.relationship(Relationship.USER_ROLE, backref="user", cascade="save-update, merge, delete", lazy=True)
    rights = db.relationship(Relationship.USER_RIGHT, backref="user", cascade="save-update, merge, delete", lazy=True)
    token = db.relationship(Relationship.TOKEN, backref="user", cascade="save-update, merge, delete", lazy=True)
    digitalisat_comments = db.relationship(Relationship.DIGITALISAT_COMMENTS, backref="user",
                                           cascade="save-update, merge", lazy=True)

    @property
    def get_roles(self):
        """ Get a list of roles for this user."""
        return [role.role_id for role in self.roles if role]

    @property
    def get_rights(self):
        """ Get a list of roles for this user."""
        return [right.right_id for right in self.rights]

    @property
    def get_token(self):
        """Get user token if any, otherwise returns None."""
        token_model = TokenModel.find_by_user_id(self.user_id)
        return token_model[0].token if token_model else None

    # this method is necessary for the test assertion.
    def get_id(self):
        return self.user_id

    @map_to_ts_style()
    def to_dict(self):
        """
        Convert UserModel into a dictionary, this way we can convert it to a JSON response.

        :return: A clean dictionary form of this model.
        """
        # convert columns to dict
        dto = super().to_dict()
        dto["password"] = None
        # add roles
        dto["roles"] = self.get_roles
        # add rights
        dto["rights"] = self.get_rights
        # add token
        dto["token"] = self.get_token
        return dto

    @classmethod
    @map_to_py_style()
    def from_dict(cls, dto: dict):
        return super().from_dict(dto)

    def has_valid_password(self, password):
        """
        Verify if user has a valid password.

        :param password: The password to be verify.
        :return: True if password is valid, False otherwise.
        """
        return app_utils.check_password(self.password, password)

    def has_role(self, role_id: str):
        return role_id in self.get_roles

    def has_right(self, right_id: str):
        return right_id in self.get_rights

    def add_role(self, role_id: str, current_user_id=None):
        """
        Add role to this user.

        Important: This will not be added to the database until user is saved.

        :param role_id: The role id, e.g: "ROLE_USER".
        :param current_user_id: The current id of the user that is making this change.
        """
        if RoleModel.is_valid_role(role_id) and not self.has_role(role_id):
            user_role = UserRoleModel(user_id=self.user_id, role_id=role_id, lastchange_by=current_user_id)
            self.roles.append(user_role)

    def add_right(self, right_id: str, current_user_id=None):

        if not self.has_role(right_id):
            user_right = UserRightModel(user_id=self.user_id, right_id=right_id, lastchange_by=current_user_id)
            self.rights.append(user_right)

    def add_roles(self, role_ids: List[str], current_user_id=None):
        """
        Add roles to this user.

        Important: This will not be added to the database until user is saved.

        :param role_ids: A list of role's ids, e.g: ["ROLE_USER", "ROLE_ADMIN"].
        :param current_user_id: The current id of the user that is making this change.
        """
        for role_id in role_ids:
            self.add_role(role_id, current_user_id)

    def add_rights(self, right_ids: List[str], current_user_id=None):
        for right_id in right_ids:
            self.add_right(right_id, current_user_id)

    def _delete_roles(self):
        """
        This will remove all roles from this user at the database.
        """
        for role in self.roles:
            role.delete()

    def _delete_rights(self):
        for right in self.rights:
            right.delete()

    @classmethod
    def create_user(cls, user_dict: dict, current_user_id=None):
        """
        This will create a new user, with new id and encrypted password.

        Import: You must use save() to storage it in the database.

        :param user_dict: A dictionary representation of the user. The dictionary must contain
            keys with the fields of UserModel table.
        :param current_user_id: (Optional) The current user id that is creating this user.
        :return: A new UserModel.
        """
        user: UserModel = cls.from_dict(user_dict)
        user.user_id = app_utils.generate_id(16)
        if not user.password:
            raise exceptions.CreateEntityError("Kein Password für den Nutzer festgelegt!")
        user.password = app_utils.encrypt_password(user.password)

        # Add role relational field.
        role_ids = user_dict.get("roles", [])
        right_ids = user_dict.get("rights", [])
        if len(role_ids) == 0 or len(right_ids) == 0:
            raise exceptions.RoleNotFound("Dem Nutzer muss mindestens eine Rolle/Rights zugewiesen werden.")
        user.add_roles(role_ids=role_ids, current_user_id=current_user_id)
        user.add_rights(right_ids=right_ids, current_user_id=current_user_id)

        return user

    @classmethod
    def update_user(cls, user_dict: dict, current_user_id=None, is_self_update=False):
        """
        Update the current user. After invoke this method with is_self_update = False all roles from this
        user will be deleted in the database. You must save it to add the new roles at the database.

        Import: You must use save() to store it in the database.

        :param user_dict: A dictionary representation of the user. The dictionary must contain
            keys with the fields of UserModel table.
        :param current_user_id: (Optional) The current user id that is creating this user.
        :param is_self_update: (Optional) Set to True if user is updating itself, False (default) otherwise.
        :return: The updated user or None if user if not valid.
        """
        user: UserModel = cls.from_dict(user_dict)
        user_id = user.user_id
        valid_user: UserModel = UserModel.find_by_id(user_id)
        if not valid_user:
            return None
        # Verify if self update is from the same user, if not return None.
        if is_self_update:
            if valid_user.user_id != current_user_id:
                return None

        # Update a valid user.
        valid_user.username = user.username
        valid_user.forename = user.forename
        valid_user.surname = user.surname
        # Update password only if it doesn't match.
        if user.password is not None and valid_user.password != user.password:
            valid_user.password = app_utils.encrypt_password(user.password)

        # only update roles if is not self update. (Only admin can update roles.)
        if not is_self_update:
            # Update role relational field.
            role_ids = user_dict.get("roles", [])
            right_ids = user_dict.get("rights", [])
            if not (role_ids or right_ids):
                raise exceptions.RoleNotFound("Dem Nutzer muss mindestens eine Rolle/Rights zugewiesen sein.")

            # delete all roles
            valid_user._delete_roles()
            # add new ones.
            valid_user.add_roles(role_ids=role_ids, current_user_id=current_user_id)

            # delete all rights
            valid_user._delete_rights()
            # add new ones.
            valid_user.add_rights(right_ids=right_ids, current_user_id=current_user_id)

        return valid_user

    # Queries for this model.
    @classmethod
    def find_by_username(cls, username: str):
        """
        Try to find an user: :class:`UserModel` by the given username.

        :param username: The username to be found.
        :return: The found UserModel or None if not found.
        """
        user: UserModel = cls.find_by(username=username)
        if user:
            return user

        return None


# Called when either security or current_user is required.
# Import this must be locate at the same file as UserModel
@login_manager.request_loader
def load_user(request):
    # X-Access-Token come from the client side.
    # This header is add to requests at the token.interceptor at the Angular side.
    token = request.headers.get('X-Access-Token')
    if token:
        token_model = TokenModel.find_by(token=token)
        if token_model:
            return token_model.user  # This is possible because of backref = user.
        else:
            app_logger.warning("The token {} does not exist in the database.".format(token))
            return None

    app_logger.warning("Header request does not include a token.")
    return None
