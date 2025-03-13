import unittest

from flaskapp.models import SearchCategoryModel
from flaskapp.search import SearchCategorySearch
from flaskapp.structures.structures import SearchResult
from tests.test_models.db_setup import DbSetup


class TestSearchCategoryModel(DbSetup):

    def test_create_search_category(self):
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(0, len(search_categories))
        search_category = self.persist_search_category()
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(1, len(search_categories))
        saved_search_category: SearchCategoryModel = search_categories[0]
        self.assertEqual(search_category, saved_search_category)

    def test_search_search_category(self):
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(0, len(search_categories))
        search_category = self.persist_search_category()
        search_category_search = SearchCategorySearch()
        search_result: SearchResult = SearchCategoryModel.search(search_category_search)
        self.assertEqual(1, len(search_result.resultList))
        saved_search_category: SearchCategoryModel = search_result.resultList[0]
        self.assertEqual(search_category, saved_search_category)

    def test_update_search_category(self):
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(0, len(search_categories))
        search_category = self.persist_search_category()
        search_category_id = search_category.id
        search_category: SearchCategoryModel = SearchCategoryModel.find_by_id(search_category_id)
        self.assertEqual(search_category_id, search_category.id)
        name_2 = "B"
        search_category.name = name_2
        search_category.save()
        search_category = SearchCategoryModel.find_by_id(search_category_id)
        self.assertEqual(name_2, search_category.name)

    def test_delete_search_category(self):
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(0, len(search_categories))
        search_category = self.persist_search_category()
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(1, len(search_categories))
        search_category.delete()
        search_categories = SearchCategoryModel.get_all()
        self.assertEqual(0, len(search_categories))


if __name__ == '__main__':
    unittest.main()
