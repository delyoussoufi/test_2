import unittest

from flaskapp.models import ScopeDataModel
from tests.test_models.db_setup import DbSetup


class TestScopeDataModel(DbSetup):

    def validate_scope_data(self):
        scope_data_items = ScopeDataModel.get_all()
        self.assertEqual(0, len(scope_data_items))
        digitalisat = self.persist_digitalisat(self.target_folder.id)
        scope_data = self.persist_scope_data(digitalisat.id)
        scope_data_items = ScopeDataModel.get_all()
        self.assertEqual(1, len(scope_data_items))
        return scope_data

    def test_create_scope_data(self):
        scope_data = self.validate_scope_data()
        saved_scope_data = ScopeDataModel.get_all()[0]
        self.assertEqual(scope_data, saved_scope_data)

    def test_update_scope_data(self):
        scope_data = self.validate_scope_data()
        title = scope_data.title
        scope_data = ScopeDataModel.find_by_id(scope_data.id)
        self.assertEqual(title, scope_data.title)
        title = "Test, Aaron"
        scope_data.title = title
        scope_data.save()
        scope_data = ScopeDataModel.find_by_id(scope_data.id)
        self.assertEqual(title, scope_data.title)

    def test_delete_scope_data(self):
        scope_data = self.validate_scope_data()
        scope_data.delete()
        scope_data_items = ScopeDataModel.get_all()
        self.assertEqual(0, len(scope_data_items))


if __name__ == '__main__':
    unittest.main()
