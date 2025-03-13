import unittest

from flaskapp.models import DigitalisatModel, ClassificationStatusModel, ClassificationStatus
from flaskapp.models.enums import DigitalisatStatus
from tests.test_models.db_setup import DbSetup


class TestDigitalisatModel(DbSetup):

    def validate_digitalisat(self):
        digitalisate = DigitalisatModel.get_all()
        self.assertTrue(len(digitalisate) == 0)
        digitalisat = self.persist_digitalisat(self.target_folder.id)
        digitalisat.scope_data = self.get_scope_data(digitalisat_id=digitalisat.id)
        digitalisate = DigitalisatModel.get_all()
        self.assertEqual(1, len(digitalisate))
        return digitalisat

    def test_create_digitalisat(self):
        digitalisat = self.validate_digitalisat()
        saved_digitalisat = DigitalisatModel.get_all()[0]
        self.assertEqual(digitalisat, saved_digitalisat)
        self.assertEqual(0, digitalisat.number_of_images())

    def test_get_idles(self):
        digitalisat = self.validate_digitalisat()
        search_digitalisate = DigitalisatModel.get_idles()
        self.assertEqual(1, len(search_digitalisate))
        self.assertEqual(digitalisat, search_digitalisate[0])

    def test_get_downloading_images(self):
        digitalisat = self.validate_digitalisat()
        search_digitalisate = DigitalisatModel.get_idles()
        self.assertEqual(1, len(search_digitalisate))
        self.assertEqual(digitalisat, search_digitalisate[0])
        digitalisat.status = DigitalisatStatus.DOWNLOADING_IMAGES
        digitalisat.save()
        search_digitalisate = DigitalisatModel.get_downloading_images_status()
        self.assertEqual(1, len(search_digitalisate))
        self.assertEqual(digitalisat, search_digitalisate[0])

    def test_find_digitalisate_by_target_folder_id(self):
        digitalisat = self.validate_digitalisat()
        digitalisat.bestand_id = None
        digitalisat.save()
        digitalisate = DigitalisatModel.find_digitalisate_by_target_folder_id(self.target_folder.id)
        self.assertEqual(1, len(digitalisate))

    def test_update_digitalisat(self):
        digitalisat = self.validate_digitalisat()
        folder_name = digitalisat.folder_name
        digitalisat = DigitalisatModel.find_by_id(digitalisat.id)
        self.assertEqual(folder_name, digitalisat.folder_name)
        folder_name = "blha_10a_domkapitel_havelberg_u_12_ID896172"
        digitalisat.folder_name = folder_name
        digitalisat.save()
        digitalisat = DigitalisatModel.find_by_id(digitalisat.id)
        self.assertEqual(folder_name, digitalisat.folder_name)

    def test_delete_digitalisat(self):
        digitalisat = self.persist_digitalisat(self.target_folder.id)
        digitalisat.delete()
        digitalisate = DigitalisatModel.get_all()
        self.assertEqual(0, len(digitalisate))

    def test_to_dict(self):
        digitalisat = self.validate_digitalisat()
        digitalisat_dict = digitalisat.to_dict()
        self.assertIsNotNone(digitalisat_dict)
        self.assertEqual(digitalisat.signature, digitalisat_dict["signature"])
        self.assertEqual(digitalisat.scope_data.digitalisat_id, digitalisat_dict["scopeData"]["digitalisatId"])

    def test_get_digitalisate_with_open_or_no_classification(self):
        digitalisat = self.persist_digitalisat(self.target_folder.id)
        digitalisat.status = DigitalisatStatus.FINISHED
        digitalisat.save()
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification()
        # no classification is expected.
        self.assertEqual(1, len(digitalisate))
        self.assertEqual(digitalisat, digitalisate[0])

        search_category = self.persist_search_category()
        digitalisat.add_classification_status(search_category_id=search_category.id, status=ClassificationStatus.OPEN)
        digitalisat.save()
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification()
        # open classification expected.
        self.assertEqual(1, len(digitalisate))

        # for a given search category
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification(category_id=search_category.id)
        self.assertEqual(1, len(digitalisate))

        [
            print(f"entity: {m}")
            for m in DigitalisatModel.get_digitalisate_with_open_or_no_classification(search_category.id)
        ]

        # for a given search category
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification(category_id='test')
        self.assertEqual(1, len(digitalisate))

        # close classification status.
        csm = ClassificationStatusModel.find_by_id(digitalisat.id, search_category.id)
        self.assertIsNotNone(csm)
        csm.status = ClassificationStatus.CLOSED
        self.assertTrue(csm.save())

        # no digitalisate expected with open classification.
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification()
        self.assertEqual(0, len(digitalisate))

        # no digitalisate expected with open classification.
        digitalisate = DigitalisatModel.get_digitalisate_with_open_or_no_classification(category_id=search_category.id)
        self.assertEqual(0, len(digitalisate))





if __name__ == '__main__':
    unittest.main()
