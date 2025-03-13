# include models class name here.
class Relationship:
    """
    Keep track of models class name for being used in relational tables.
    """
    USER_ROLE = "UserRoleModel"
    USER_RIGHT = "UserRightModel"
    USER = "UserModel"
    ROLE = "RoleModel"
    TOKEN = "TokenModel"
    SEARCH_TERM = "SearchTermModel"
    BLACKLIST_TERM = "BlacklistTermModel"
    NON_RELEVANT_TERM = "NonRelevantTermModel"
    DIGITALISAT = "DigitalisatModel"
    DIGITALISAT_IMAGE = "DigitalisatImageModel"
    SCOPE_DATA = "ScopeDataModel"
    CLASSIFICATION_STATUS = "ClassificationStatusModel"
    IMAGE_CLASSIFICATION = "ImageClassificationModel"
    DIGITALISAT_COMMENTS = "DigitalisatCommentsModel"
    DIGITALISAT_CLASSIFICATION_LOCK = "DigitalisatClassificationLockModel"
    DIGITALISAT_IMAGE_OCR = "DigitalisatImageOcrModel"
    VORGANG = "VorgangModel"
    VORGANG_IMAGES = "VorgangImagesModel"


# Include the name of tables from your data base. Use this to map table's name.
# This Avoid possibles circular imports from getting __tablename__ from models.
class TableNames:
    """
    Name of structures (S) or tables (T) in your database.
    Important: The names must match the table's name in your database.
    """
    T_APPLICATION_PARAM = "t_application_param"
    T_ARCHIVALIEN_ARTEN = "t_archivalien_arten"
    T_VORGANG = "t_vorgang"
    T_VORGANG_IMAGES = "t_vorgang_images"
    T_SEARCH_CATEGORY = "t_search_category"
    T_SEARCH_TERM = "t_search_term"
    T_BLACKLIST_TERM = "t_blacklist_term"
    T_NON_RELEVANT_TERM = "t_non_relevant_term"
    T_EXCEPTION_LOG = "t_exception_log"
    T_USER = "t_user"
    T_TOKEN = "t_access_tokens"
    S_ROLES = "s_roles"
    S_RIGHTS = "s_rights"
    T_USER_ROLES = "t_user_roles"
    T_USER_RIGHTS = "t_user_rights"
    T_ROLES_RIGHTS = "t_roles_rights"
    T_TARGET_FOLDERS = "t_target_folders"
    T_BESTAND_WATCHER = "t_bestand_watcher"
    T_DIGITALISAT = "t_digitalisat"
    T_DIGITALISAT_IMAGE = "t_digitalisat_image"
    T_SCOPE_DATA = "t_scope_data"
    T_DIGITALISAT_IMAGE_OCR = "t_digitalisat_image_ocr"
    T_CLASSIFICATION_STATUS = "t_classification_status"
    T_IMAGE_CLASSIFICATION = "t_image_classification"
    T_DIGITALISAT_COMMENTS = "t_digitalisat_comment"
    T_CLASSIFYING_JOB = "t_classifying_job"
    T_DIGITALISAT_CLASSIFICATION_LOCK = "t_digitalisat_classification_lock"


class Role:
    """ Possible roles for the user."""
    USER = "ROLE_USER"
    RESERVATION = "ROLE_RESERVATION"
    ORDER = "ROLE_ORDER"
    ADMIN = "ROLE_ADMIN"
    VIEWER = "ROLE_VIEWER"


class Right:

    """ Possible rights for the user."""
    APP_SETTINGS = "RIGHT_APP_SETTINGS"
    BESTANDE_ADD = "RIGHT_BESTANDE_ADD"
    CATEGORY_EDIT = "RIGHT_CATEGORY_EDIT"
    CATEGORY_VIEW = "RIGHT_CATEGORY_VIEW"
    COMMENT = "RIGHT_COMMENT"
    DIGITALISATE_UPDATE = "RIGHT_DIGITALISATE_UPDATE"
    DIGITALISATE_VIEW = "RIGHT_DIGITALISATE_VIEW"
    IMAGE_UPDATE = "RIGHT_IMAGE_UPDATE"
    RECLASSIFY = "RIGHT_RECLASSIFY"
    SEARCH = "RIGHT_SEARCH"
    USER_EDIT = "RIGHT_USER_EDIT"
    VORGANG = "RIGHT_VORGANG"
    VORGANG_PDF = "RIGHT_VORGANG_PDF"


# Import models. Watch for circular dependencies.
from flaskapp.models.base_model import BaseModel
from flaskapp.models.application_param_model import ApplicationParamModel
from flaskapp.models.archivalienart_model import ArchivalienartModel
from flaskapp.models.exception_log_model import ExceptionLogModel
from flaskapp.models.vorgang_model import VorgangModel
from flaskapp.models.role_model import RoleModel
from flaskapp.models.rights_model import RightModel
from flaskapp.models.user_role_model import UserRoleModel
from flaskapp.models.roles_rights_model import RolesRightsModel
from flaskapp.models.user_right_model import UserRightModel
from flaskapp.models.token_model import TokenModel
from flaskapp.models.digitalisat_comments_model import DigitalisatCommentsModel
from flaskapp.models.user_model import UserModel
from flaskapp.models.target_folder_model import TargetFolderModel
from flaskapp.models.bestand_watcher_model import BestandWatcherModel
from flaskapp.models.digitalisat_classification_lock_model import DigitalisatClassificationLockModel
from flaskapp.models.classification_status_model import ClassificationStatusModel, ClassificationStatus
from flaskapp.models.image_classification_model import ImageClassificationModel
from flaskapp.models.digitalisat_model import DigitalisatModel
from flaskapp.models.digitalisat_image_model import DigitalisatImageModel
from flaskapp.models.scope_data_model import ScopeDataModel
from flaskapp.models.search_term_model import SearchTermModel
from flaskapp.models.blacklist_term_model import BlacklistTermModel
from flaskapp.models.non_relevant_term_model import NonRelevantTermModel
from flaskapp.models.search_category_model import SearchCategoryModel
from flaskapp.models.digitalisat_image_ocr_model import DigitalisatImageOcrModel
from flaskapp.models.classifying_job_model import ClassifyingJobStatus
