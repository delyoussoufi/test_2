from flaskapp import app_logger
from flaskapp.controllers import rest
from flaskapp.http_util import response
from flaskapp.http_util.decorators import post_from_form, query_param
from flaskapp.http_util.exceptions import PermissionDenied
from flaskapp.http_util.login_safer import safe_login
from flaskapp.models import UserModel, TokenModel


@rest.route("/authentication/authenticateUser",  methods=["POST"])
@post_from_form("username", "password")
@safe_login(error_on_block=PermissionDenied)
def login(username=None, password=None):
    user = UserModel.find_by_username(username)

    if user and user.has_valid_password(password):

        # Token exist just used it.
        token_model = TokenModel.find_by(user_id=user.user_id, get_first=True)
        if token_model:
            return response.model_to_response(user)
        else:
            # create a token for user.
            token_model = TokenModel.create_token(user.user_id)
            if token_model.save():
                app_logger.info(f"User {username} logged in successfully.")
                return response.model_to_response(user)
            else:
                app_logger.warning(f"Fail to save token for user {username}.")
                return response.empty_response()

    app_logger.info("User {} has bad credentials.".format(username))
    return response.empty_response()


@rest.route("/authentication/hasToken",  methods=["GET"])
@query_param("userToken", "userId")
def has_token(user_token=None, user_id=None):
    if user_token is not None and user_id is not None:
        atk = TokenModel.find_by_token(user_token)
        _remove_inactive_user_tokens(user_id, atk)
        if atk is not None:
            return response.bool_to_response(True)
    return response.bool_to_response(False)


def _remove_inactive_user_tokens(user_id: str, active_token: TokenModel):
    """Remove inactive token if user has more than 2 tokens.
    @param user_id
    @param active_token"""
    # Define how many tokens a user can have.
    number_of_tokens_per_user = 2
    # Only delete if it can safely compare tokens.
    if active_token is not None:
        tokens = TokenModel.find_by_user_id(user_id)
        if tokens is not None and len(tokens) > number_of_tokens_per_user:
            for token in tokens:
                if token.id != active_token.id:
                    token.delete()
