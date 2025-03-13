import re

from flask_login import current_user

from flaskapp import app_utils
from flaskapp.http_util.exceptions import AppException
from flaskapp.models import UserModel
from flaskapp.structures.dtos import ProfileDto


class UserService:

    @staticmethod
    def update_profile(profile_user: ProfileDto):
        existing_user: UserModel = UserModel.find_by_id(current_user.user_id)
        if existing_user and existing_user.user_id == profile_user.user_id:
            if profile_user.password:
                UserService.__validate_password(profile_user.password, existing_user.password)
                if profile_user.password != profile_user.repeated_password:
                    raise AppException("Die Passwörter müssen identisch sein!")
            else:
                profile_user.password = existing_user.password

            existing_user = UserModel.update_user(user_dict=profile_user.to_dict(),
                                                  current_user_id=current_user.user_id, is_self_update=True)
            existing_user.save()
            return existing_user

        raise AppException("Fehler beim Aktualisieren des Nutzerprofils!")

    @staticmethod
    def __validate_password(password: str, old_password_hash: str):
        if len(password) < 8:
            raise AppException("Das Passwort muss mindestens 8 Zeichen lang sein.")
        if not bool(re.search(".*[A-Z].*", password)):
            raise AppException("Das Passwort muss einen Großbuchstaben enthalten.")
        if not bool(re.search(".*[a-z].*", password)):
            raise AppException("Das Passwort muss einen Kleinbuchstaben enthalten.")
        if not bool(re.search(".*\\d..*", password)):
            raise AppException("Das Passwort muss eine Zahl enthalten.")
        if not bool(re.search(".*[`~!@#$%^&*()\\-_=+\\\\|\\[{\\]};:'\",<.>/?].*", password)):
            raise AppException("Das Passwort muss ein Sonderzeichen enthalten.")
        if old_password_hash and app_utils.check_password(old_password_hash, password):
            raise AppException("Das neue und alte Passwort dürfen nicht gleich sein.")

