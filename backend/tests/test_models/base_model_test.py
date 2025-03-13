import datetime
import os

from flaskapp import app_utils, bcrypt
from flaskapp.models import VorgangModel, UserRoleModel, Role, SearchCategoryModel, SearchTermModel, UserModel, \
    DigitalisatModel, TargetFolderModel, ScopeDataModel
from flaskapp.models.enums import DigitalisatStatus
from resources.sql import sql_path


class BaseModelTest:
    user_username = "user"
    user_password = "user"

    @staticmethod
    def delete_database_file():
        if os.path.isfile(sql_path + "/provenance.sqlite"):
            os.remove(sql_path + "/provenance.sqlite")

    def get_user(self) -> UserModel:
        user = UserModel()
        user.user_id = app_utils.generate_id(16)
        user.username = BaseModelTest.user_username
        user.password = bcrypt.generate_password_hash(BaseModelTest.user_password)
        user.forename = "John"
        user.surname = "Doe"
        return user

    def persist_user(self) -> UserModel:
        user = self.get_user()
        user_role = UserRoleModel(user_id=user.user_id, role_id=Role.USER, lastchange_by=user.user_id)
        user.roles.append(user_role)
        user.save()
        return user

    def get_vorgang(self) -> VorgangModel:
        vorgang: VorgangModel = VorgangModel()
        vorgang.id = app_utils.generate_id(16)
        return vorgang

    def persist_vorgang(self, digitalisat_id: str, search_category_id: str) -> VorgangModel:
        vorgang: VorgangModel = self.get_vorgang()
        vorgang.vorgangsnummer = "A1"
        vorgang.create_date = datetime.datetime.now()
        vorgang.digitalisat_id = digitalisat_id
        vorgang.search_category_id = search_category_id
        vorgang.vorgang_order = VorgangModel.get_next_order(search_category_id)
        vorgang.save()
        return vorgang

    def get_search_category(self) -> SearchCategoryModel:
        search_category: SearchCategoryModel = SearchCategoryModel()
        search_category.id = app_utils.generate_id(16)
        return search_category

    def persist_search_category(self) -> SearchCategoryModel:
        search_category: SearchCategoryModel = self.get_search_category()
        search_category.name = "A1"
        search_category.description = "Blablabla"
        search_category.save()
        return search_category

    def get_search_term(self, search_category_id: str) -> SearchTermModel:
        search_term: SearchTermModel = SearchTermModel()
        search_term.id = app_utils.generate_id(16)
        search_term.category_id = search_category_id
        return search_term

    def persist_search_term(self, search_category_id: str)-> SearchTermModel:
        search_term: SearchTermModel = self.get_search_term(search_category_id)
        search_term.search_value = "Frankenstein"
        search_term.save()
        return search_term

    def get_target_folder(self, path: str) -> TargetFolderModel:
        targetFolder = TargetFolderModel()
        targetFolder.id = app_utils.generate_id(16)
        targetFolder.path = path
        targetFolder.active = True
        return targetFolder

    def persist_target_folder(self, path: str) -> TargetFolderModel:
        target_folder = self.get_target_folder(path)
        target_folder.save()
        return target_folder

    def get_digitalisat(self, target_folder_id: str) -> DigitalisatModel:
        digitalisat = DigitalisatModel()
        digitalisat.id = app_utils.generate_id(16)
        digitalisat.signature = "10A Domkapitel Havelberg U 11"
        digitalisat.scope_id = "896170"
        digitalisat.folder_name = "blha_10a_domkapitel_havelberg_u_11_ID896170"
        digitalisat.sub_folder = 1
        digitalisat.expected_images = 0
        digitalisat.status = DigitalisatStatus.IDLE
        digitalisat.archivalien_arten_id = "FfQMIvWpEK"
        digitalisat.create_date = datetime.date.today()
        digitalisat.target_folder_id = target_folder_id
        return digitalisat

    def persist_digitalisat(self, target_folder_id: str) -> DigitalisatModel:
        digitalisat = self.get_digitalisat(target_folder_id)
        digitalisat.save()
        return digitalisat

    def get_scope_data(self, digitalisat_id: str) -> ScopeDataModel:
        scope_data = ScopeDataModel()
        scope_data.id = app_utils.generate_id(16)
        scope_data.digitalisat_id = digitalisat_id
        scope_data.title = "Test, Wilhelm"
        scope_data.dat_findbuch = "1941 - 1942"
        scope_data.geburtsdatum = datetime.datetime(1879, 10, 18)
        scope_data.geburtsort = "Innsbrucker Str. 41"
        scope_data.registry_signature = "O 5210 - 1590/40"
        scope_data.associates = "Enthält u. a.: Test geb. Test, Agnes Henriette. - Test, Ilse. " \
                                "- Test, Eva Charlotte Rebekka. - Test, Paul Wilhelm. - Test, Ilse Ruth Ernestine."
        return scope_data

    def persist_scope_data(self, digitalisat_id: str) -> ScopeDataModel:
        scope_data = self.get_scope_data(digitalisat_id)
        scope_data.save()
        return scope_data
