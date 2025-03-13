import os
import unittest

from flaskapp.services import DigiRequests
from tests.test_resources.images import test_resources_images_path


class TestDigiRequests(unittest.TestCase):

    # TODO Improve digi request test. Must be more robust.
    def setUp(self) -> None:
        pass
        # self.digi_requests = DigiRequests()

    # def test_get_bestand(self):
    #     bestand_dict: dict = self.digi_requests.get_bestand("MjxqJEaTawVVxpgr")
    #     self.assertEqual(bestand_dict.get("name", None),
    #                      "Rep. 10B Zisterzienserinnenkloster/Stift Heiligengrabe A - Karten")
    #
    # def test_get_digitalisate(self):
    #
    #     bestand_dict: dict = self.digi_requests.get_bestand("zPUmcrBgRHMqZYpj")
    #     self.assertEqual(bestand_dict.get("name", None), "Hochbau")
    #     digitalisate = self.digi_requests.get_digitalisate(bestand_dict.get("id"))
    #     print(digitalisate)
    #
    # def test_get_digitalisate_stream(self):
    #
    #     bestand_dict: dict = self.digi_requests.get_bestand("zPUmcrBgRHMqZYpj")
    #     self.assertEqual(bestand_dict.get("name", None), "Hochbau")
    #     for dto in self.digi_requests.get_digitalisate_stream(bestand_dict.get("id")):
    #         print(dto)
    #
    # def test_get_digitalisat_images(self):
    #
    #     bestand_dict: dict = self.digi_requests.get_bestand("Hochbau")
    #     self.assertEqual(bestand_dict.get("name", None), "Hochbau")
    #     digitalisate = self.digi_requests.get_digitalisate(bestand_dict.get("id"))
    #     digitalisat = digitalisate[0]
    #     d_images = self.digi_requests.get_digitalisat_images(digitalisat.get("id"))
    #     print(d_images)
    #
    # def test_get_image_file(self):
    #     bestand_dict: dict = self.digi_requests.get_bestand("Hochbau")
    #     self.assertEqual(bestand_dict.get("name", None), "Hochbau")
    #     digitalisate = self.digi_requests.get_digitalisate(bestand_dict.get("id"))
    #     digitalisat = digitalisate[0]
    #     d_images = self.digi_requests.get_digitalisat_images(digitalisat.get("id"))
    #     image = d_images[0]
    #     output_dir = test_resources_images_path
    #     image_path, _ = self.digi_requests.get_image_file(image.get("id"), output_dir=output_dir)
    #     self.assertTrue(os.path.isfile(image_path))
    #     os.remove(image_path)
    #     self.assertFalse(os.path.isfile(image_path))


if __name__ == '__main__':
    unittest.main()
