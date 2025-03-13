# User APIs.
from typing import List

from flask_login import current_user

from flaskapp import app_logger
from flaskapp.controllers import users
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure, post, query
from flaskapp.http_util.exceptions import UserNotFound, AppException
from flaskapp.models import UserModel, Role, RoleModel, RightModel, RolesRightsModel, Right
from flaskapp.search import UserSearch
from flaskapp.structures.structures import SearchResult


def __is_username_taken(username: str) -> bool:
    user = UserModel.find_by_username(username)
    if user:
        return True
    return False


@users.route("/<string:user_id>", methods=["GET"])
@secure(Right.USER_EDIT)
def get_user(user_id: str):
    user: UserModel = UserModel.find_by_id(user_id)
    if user:
        return response.model_to_response(user)

    return response.empty_response()


@users.route("/roles", methods=["GET"])
@secure(Right.USER_EDIT)
def get_roles():
    roles: List[RoleModel] = RoleModel.get_all(order_by=RoleModel.label)
    return response.model_to_response(roles)


@users.route("/rights", methods=["GET"])
@secure(Right.USER_EDIT)
def get_rights():
    rights: List[RightModel] = RightModel.get_all(order_by=RightModel.label)
    return response.model_to_response(rights)


@users.route("/rightsByRole/<string:role_id>", methods=["GET"])
@secure(Right.USER_EDIT)
def get_rights_by_role(role_id: str):
    rights: List[str] = [model.right_id for model in RolesRightsModel.find_by(role_id=role_id, get_first=False)]
    return response.string_to_response(rights)


@users.route("/all", methods=["GET"])
@secure(Right.USER_EDIT)
def get_users():
    all_users: List[UserModel] = UserModel.get_all()

    if all_users:
        return response.model_to_response(all_users)

    return response.empty_response()


@users.route("/search", methods=["GET"])
@secure(Right.USER_EDIT)
@query(UserSearch)
def search_user(user_search: UserSearch):
    search_result: SearchResult = UserModel.search(user_search)
    return response.model_to_response(search_result)


@users.route("/username/<string:username>", methods=["GET"])
@secure(Right.USER_EDIT)
def get_user_by_username(username: str):
    user = UserModel.find_by_username(username)

    if user:
        return response.model_to_response(user)

    return response.empty_response()


@users.route("/isTaken/<string:username>", methods=["GET"])
@secure(Right.USER_EDIT)
def is_taken(username: str):
    user_exist = __is_username_taken(username)
    return response.bool_to_response(user_exist)


@users.route("/create", methods=["POST"])
@secure(Right.USER_EDIT)
@post()
def create_user(user: dict):
    # create a user model from user data.
    user_model = UserModel.create_user(user, current_user.user_id)

    # Check if user with the same username don't exist.
    if __is_username_taken(user_model.username):
        raise AppException("Ein Nutzer mit diesem Benutzernamen existiert bereits!")

    created = user_model.save()

    return response.bool_to_response(created)


@users.route("", methods=["PUT"])
@secure(Right.USER_EDIT)
@post()
def update_user(user: dict):
    # update user
    updated_user = UserModel.update_user(user, current_user.user_id)

    if not updated_user:
        raise UserNotFound("Der Nutzer existiert nicht.")

    if not updated_user.save():
        raise AppException("Der Nutzer konnte nicht aktualisiert werden.")
    return response.model_to_response(updated_user)


@users.route("/<string:user_id>", methods=["DELETE"])
@secure(Right.USER_EDIT)
def delete_user(user_id):
    user: UserModel = UserModel.find_by_id(user_id)
    if not user:
        raise UserNotFound("The user id {} doesn't exist".format(user_id))

    deleted = user.delete()
    if deleted:
        app_logger.info("User {} has been deleted".format(user.username))
    else:
        app_logger.warning("User {} couldn't be deleted.".format(user.username))

    return response.bool_to_response(deleted)
