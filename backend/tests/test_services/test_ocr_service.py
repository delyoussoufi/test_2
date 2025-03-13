import os.path
import unittest

from flaskapp.services.ocr_service import OcrDataParse
from flaskapp.structures import OcrData
from tests.test_resources.images_ocr import test_resources_images_ocr_path


class TestOcrDataParse(unittest.TestCase):

    def setUp(self):
        self.ocr_alto_file_xml = os.path.join(test_resources_images_ocr_path, "BXZmvQxPXwTvmPJT.xml")
        self.ocr_alto_file_json = os.path.join(test_resources_images_ocr_path, "BXZmvQxPXwTvmPJT.json")

    def test_parse_alto_xml(self):
        ocr_data: OcrData = OcrDataParse.parse_alto_xml(self.ocr_alto_file_xml)
        self.assertEqual(64, len(ocr_data.words))
        self.assertEqual("Oberfinanzkaffe", ocr_data.words[0].text)

    def test_parse_alto_json(self):
        ocr_data: OcrData = OcrDataParse.parse_alto_json(self.ocr_alto_file_json)
        self.assertEqual(61, len(ocr_data.words))
        self.assertEqual("Oberfinanzkaffe", ocr_data.words[0].text)

    def test_compare_xml_json(self):
        ocr_data_json: OcrData = OcrDataParse.parse_alto_json(self.ocr_alto_file_json)
        ocr_data_xml: OcrData = OcrDataParse.parse_alto_xml(self.ocr_alto_file_xml)
        print(ocr_data_json)
        print(ocr_data_xml)


if __name__ == '__main__':
    unittest.main()
