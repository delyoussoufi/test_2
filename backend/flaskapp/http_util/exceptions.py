import http
import traceback

from flask import jsonify, Blueprint


# Exceptions Classes
from sqlalchemy.exc import SQLAlchemyError

from flaskapp import db


class AppException(Exception):

    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class UserNotFound(AppException):
    status_code = http.HTTPStatus.NOT_FOUND


class EntityNotFound(AppException):
    status_code = http.HTTPStatus.NOT_FOUND


class CreateEntityError(AppException):

    status_code = http.HTTPStatus.NOT_ACCEPTABLE


class PermissionDenied(AppException):

    status_code = http.HTTPStatus.UNAUTHORIZED


class RoleNotFound(AppException):

    status_code = http.HTTPStatus.FAILED_DEPENDENCY


class ForbiddenFileFormat(AppException):

    status_code = http.HTTPStatus.FORBIDDEN


class FileAlreadyExists(AppException):

    status_code = http.HTTPStatus.CONFLICT


class ActiveFolderNotFound(AppException):

    status_code = http.HTTPStatus.NOT_FOUND


class FileNotFound(AppException):

    status_code = http.HTTPStatus.NOT_FOUND


def error_to_response(error: AppException):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def save_error_to_log(e):
    from flaskapp.services import AdministrationService
    exception_log = AdministrationService.create_exception_log(e)
    exception_log.save()


# Register exceptions in the app.
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(SQLAlchemyError)
def handle_sql_server_error(e):
    db.session.rollback()  # if a SQLAlchemyError occur we need to rollback() db before save the exception_log.
    save_error_to_log(e)
    return error_to_response(AppException(str(e)))


@errors.app_errorhandler(Exception)
def handle_internal_server_error(e):
    print(traceback.format_exc())
    save_error_to_log(e)

    return error_to_response(AppException(str(e)))


@errors.app_errorhandler(AppException)
def handle_app_exception(error: AppException):
    return error_to_response(error)


@errors.app_errorhandler(UserNotFound)
def handle_user_not_found(error: UserNotFound):
    return error_to_response(error)


@errors.app_errorhandler(EntityNotFound)
def handle_entity_not_found(error: EntityNotFound):
    return error_to_response(error)


@errors.app_errorhandler(CreateEntityError)
def handle_create_entity_error(error: CreateEntityError):
    return error_to_response(error)


@errors.app_errorhandler(PermissionDenied)
def handle_permission_denied(error: PermissionDenied):
    return error_to_response(error)


@errors.app_errorhandler(RoleNotFound)
def handle_role_not_found(error: RoleNotFound):
    return error_to_response(error)


@errors.app_errorhandler(ForbiddenFileFormat)
def handle_forbidden_file_format(error: ForbiddenFileFormat):
    return error_to_response(error)


@errors.app_errorhandler(FileAlreadyExists)
def handle_file_already_exists(error: FileAlreadyExists):
    return error_to_response(error)


@errors.app_errorhandler(ActiveFolderNotFound)
def handle_active_folder_not_found(error: ActiveFolderNotFound):
    return error_to_response(error)


@errors.app_errorhandler(FileNotFound)
def handle_file_not_found(error: FileNotFound):
    return error_to_response(error)
