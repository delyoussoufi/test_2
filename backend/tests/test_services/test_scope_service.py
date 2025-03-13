import unittest

from flaskapp.config import DevelopmentTestConfig
from flaskapp.services import ScopeService
from flaskapp.services.scope_service import DigitalisatScopeInfo
from flaskapp.utils import DateUtils


class TestScopeService(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     app = create_app(config_class=DevelopmentTestConfig)
    #     app.app_context().push()

    def setUp(self) -> None:
        self.scope_service = ScopeService(DevelopmentTestConfig)
        self.scope_id = 2002405
        self.signatur = "36A (II) 27787"
        self.title = "Nachmann, Margot"

    def test_get_signature(self):
        """
        Test of get_signature method, of class scope service.
        """
        result = self.scope_service.get_signature(self.scope_id)
        self.assertEqual(self.signatur, result)
        self.scope_id = 000000
        result = self.scope_service.get_signature(self.scope_id)
        self.assertEqual(None, result)

    def test_get_id(self):
        """
        Test of get_id method, of class scope service.
        """
        result = self.scope_service.get_id(self.signatur)
        self.assertEqual(self.scope_id, result)
        self.signatur = "fake sig"
        result = self.scope_service.get_id(self.signatur)
        self.assertEqual(None, result)

    def test_get_title(self):
        result = self.scope_service.get_title(self.scope_id)
        self.assertEqual(self.title, result)
        self.scope_id = 000000
        result = self.scope_service.get_signature(self.scope_id)
        self.assertEqual(None, result)

    def test_get_gsft_obj_dtl(self):
        """
        Test of get_gsft_obj_dtl method, of class scope service.
        """

        # Set mapper to bypass AppParam.
        DigitalisatScopeInfo.SCOPE_ELEMENTS_MAPPER = {
            1: 'title',
            10158: 'geburtsname',
            10100: 'dat_findbuch',
            4: 'geburtsdatum',
            10160: 'geburtsort',
            10164: 'wohnort',
            18: 'registry_signature',
            8: 'associates',
        }

        results = self.scope_service.get_gsft_obj_dtl(self.scope_id)
        dsi = DigitalisatScopeInfo(self.scope_id, self.signatur)
        dsi.map_gsft_objs_dtl(results)

        expect_dsi = DigitalisatScopeInfo(self.scope_id, self.signatur)
        expect_dsi.title = "Nachmann, Margot"
        expect_dsi.geburtsname = "Nawratzki"
        expect_dsi.dat_findbuch = "1941 - 1945"
        expect_dsi.geburtsdatum = DateUtils.convert_german_string_to_date("22.11.1906")
        expect_dsi.geburtsort = "Berlin"
        expect_dsi.wohnort = "Bayreuther Straße 26, Berlin"
        expect_dsi.registry_signature = "O 5210 - 368/43"
        expect_dsi.associates = None

        self.assertEqual(expect_dsi.to_dict().keys(), dsi.to_dict().keys())
        self.assertEqual(expect_dsi, dsi)

        scope_id_test_year_out_of_range = 1976662
        results = self.scope_service.get_gsft_obj_dtl(scope_id_test_year_out_of_range)
        dsi = DigitalisatScopeInfo(scope_id_test_year_out_of_range, '36A (II) 2008')
        dsi.map_gsft_objs_dtl(results)
        self.assertIsNotNone(dsi)


if __name__ == '__main__':
    unittest.main()
