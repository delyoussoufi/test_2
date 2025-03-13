import os.path
import shutil
import unittest

from flaskapp.services import DigitalisatService
from tests.resources import resources_path


class TestDigitalisatService(unittest.TestCase):
    target_folder = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.target_folder = os.path.join(resources_path, "test_count")
        if not os.path.isdir(cls.target_folder):
            os.mkdir(cls.target_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.isdir(cls.target_folder):
            shutil.rmtree(cls.target_folder)

    @classmethod
    def create_sub_dirs(cls, quantity: int):
        for i in range(quantity):
            sub_dir = os.path.join(cls.target_folder, str(i + 1))
            if not os.path.isdir(sub_dir):
                os.mkdir(sub_dir)

    def test_create_sub_folder(self):
        sub_folder = DigitalisatService.create_sub_folder(self.target_folder, limit=1)
        self.assertEqual(sub_folder, os.path.join(self.target_folder, '1'))

        self.create_sub_dirs(quantity=10)

        sub_folder = DigitalisatService.create_sub_folder(self.target_folder, limit=1)
        self.assertEqual(sub_folder, os.path.join(self.target_folder, '10'))


if __name__ == '__main__':
    unittest.main()
