import unittest

from flaskapp.models import SearchTermModel
from tests.test_models.db_setup import DbSetup


class TestSearchTermModel(DbSetup):

    def test_create_search_term(self):
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(0, len(search_terms))
        search_category = self.persist_search_category()
        search_term = self.persist_search_term(search_category.id)
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(1, len(search_terms))
        saved_search_term: SearchTermModel = search_terms[0]
        self.assertEqual(search_term, saved_search_term)

    def test_update_search_category(self):
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(0, len(search_terms))
        search_category = self.persist_search_category()
        search_term = self.persist_search_term(search_category.id)
        search_term_id = search_term.id
        search_term: SearchTermModel = SearchTermModel.find_by_id(search_term_id)
        self.assertEqual(search_term_id, search_term.id)
        value_2 = "Igor"
        search_term.search_value = value_2
        search_term.save()
        search_term = SearchTermModel.find_by_id(search_term_id)
        self.assertEqual(value_2, search_term.search_value)

    def test_delete_search_term(self):
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(0, len(search_terms))
        search_category = self.persist_search_category()
        search_term = self.persist_search_term(search_category.id)
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(1, len(search_terms))
        search_term.delete()
        search_terms = SearchTermModel.query.filter().all()
        self.assertEqual(0, len(search_terms))


if __name__ == '__main__':
    unittest.main()
