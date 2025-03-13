import os.path
import shutil
import tempfile
import unittest

from flaskapp import create_app, db
from flaskapp.config import DevelopmentTestConfig
from tests.test_models.base_model_test import BaseModelTest
from tests.test_models.db_test_utils import DbTestUtils


class DbSetup(unittest.TestCase, BaseModelTest):

    @classmethod
    def setUpClass(cls) -> None:
        BaseModelTest.delete_database_file()
        app = create_app(config_class=DevelopmentTestConfig)
        app.app_context().push()

    def setUp(self) -> None:
        DbTestUtils.create_database_tables()
        self.user = self.persist_user()
        self.target_folder_file_path = self.get_temp_directory("targetFolder")
        self.target_folder = self.persist_target_folder(self.target_folder_file_path)

    def tearDown(self) -> None:
        db.close_all_sessions()
        db.engine.dispose()
        self.delete_database_file()
        if self.target_folder_file_path and os.path.isdir(self.target_folder_file_path):
            shutil.rmtree(self.target_folder_file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        db.close_all_sessions()
        db.engine.dispose()
        cls.delete_database_file()

    def get_temp_directory(self, prefix: str) -> str:
        self.temp_folder_path = tempfile.mkdtemp(prefix=prefix)
        return self.temp_folder_path


if __name__ == '__main__':
    unittest.main()
