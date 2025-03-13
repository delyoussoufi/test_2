# User APIs.

from flaskapp.controllers import rest
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import query_param, post, secure
from flaskapp.http_util.exceptions import AppException
from flaskapp.models import UserModel
from flaskapp.services import UserService
from flaskapp.structures.dtos import ProfileDto


@rest.route("/profile", methods=["GET"])
@secure()
@query_param("username")
def profile(username: str):
    user = UserModel.find_by_username(username)
    if user is None:
        raise AppException("Nutzer konnte nicht gefunden werden.")

    return response.model_to_response(user)


@rest.route("/profile/update", methods=["POST"])
@secure()
@post(class_to_map=ProfileDto)
def update_profile(profile_dto: ProfileDto):
    if profile_dto is None:
        raise AppException("Nutzer konnte nicht gefunden werden.")
    user = UserService.update_profile(profile_dto)
    # authenticationController.refreshAuthenticatedUser();
    return response.model_to_response(user)
