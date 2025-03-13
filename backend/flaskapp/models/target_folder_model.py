from flaskapp import db
from flaskapp.http_util.exceptions import AppException
from flaskapp.models import BaseModel, TableNames, Relationship


# TODO: Cacheable
class TargetFolderModel(db.Model, BaseModel):
    __tablename__ = TableNames.T_TARGET_FOLDERS

    LIMIT_OF_DIGITALISAT_IN_SUBFOLDER = 1000

    id = db.Column(db.String(16), primary_key=True)
    path: str = db.Column(db.String(400))
    active: bool = db.Column(db.Boolean())
    digitalisate = db.relationship(Relationship.DIGITALISAT, backref="target_folder", cascade="save-update",
                                   lazy="dynamic")

    @classmethod
    def find_active_target_folder(cls):
        target_folders = cls.find_by_filter(filters=[cls.active.__eq__(True)])
        if len(target_folders) == 1:
            return target_folders[0]
        elif len(target_folders) == 0:
            AppException("Es ist kein aktives Zielverzeichnis definiert.")
        else:
            AppException("More than one folder is active.")

    @classmethod
    def update_target_folder(cls, target_folder):
        safe_tf: TargetFolderModel = cls.find_by_id(target_folder.id)
        if safe_tf:
            safe_tf << target_folder
            safe_tf.save()

        return safe_tf

    def create_sub_folder(self):
        """
        Creates or gets the sub-folder where the digitalisat should be storage.

        :return: The sub-folder to store the digitalisat.
        """
        from flaskapp.services import DigitalisatService

        return DigitalisatService.create_sub_folder(self.path, limit=self.LIMIT_OF_DIGITALISAT_IN_SUBFOLDER)
