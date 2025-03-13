import unittest

from flaskapp.models import VorgangModel
from flaskapp.search import VorgangSearch
from flaskapp.structures.structures import SearchResult
from tests.test_models.db_setup import DbSetup


class TestVorgangModel(DbSetup):

    def create_vorgang(self) -> VorgangModel:
        digitalisat = self.persist_digitalisat(self.target_folder.id)
        search_category = self.persist_search_category()
        return self.persist_vorgang(digitalisat_id=digitalisat.id, search_category_id=search_category.id)

    def test_create_vorgang(self):
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(0, len(vorgaenge))
        vorgang = self.create_vorgang()
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(1, len(vorgaenge))
        saved_vorgang: VorgangModel = vorgaenge[0]
        self.assertEqual(vorgang, saved_vorgang)

    def test_search_vorgang(self):
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(0, len(vorgaenge))
        vorgang = self.create_vorgang()
        vorgang_search = VorgangSearch()
        search_result: SearchResult = VorgangModel.search(vorgang_search)
        self.assertEqual(1, len(search_result.resultList))
        saved_vorgang: VorgangModel = search_result.resultList[0]
        self.assertEqual(vorgang, saved_vorgang)

    def test_delete_vorgang(self):
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(0, len(vorgaenge))
        vorgang = self.create_vorgang()
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(1, len(vorgaenge))
        vorgang.delete()
        vorgaenge = VorgangModel.query.filter().all()
        self.assertEqual(0, len(vorgaenge))


if __name__ == '__main__':
    unittest.main()
