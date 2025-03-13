import os.path
import unittest

from reportlab.lib.units import mm

from flaskapp.report.searchable_pdf_builder import SearchablePdfBuilder
from flaskapp.services.ocr_service import OcrDataParse
from tests.test_resources.images import test_resources_images_path
from tests.test_resources.images_ocr import test_resources_images_ocr_path


class TestSearchablePdfBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.IMAGES_TEST_FOLDER = test_resources_images_path
        cls.OCR_TEST_FOLDER = test_resources_images_ocr_path

    def setUp(self) -> None:
        self.pdf_path = os.path.join(self.IMAGES_TEST_FOLDER, "test.pdf")
        self.pdf_b = SearchablePdfBuilder(self.pdf_path, pagesize=(1530, 2087))

    def tearDown(self) -> None:
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)
            pass

    def test_build_readable_pdf(self):

        ocr_data = OcrDataParse.parse_alto_xml(os.path.join(self.OCR_TEST_FOLDER, "hnEVsPyTxnbJuBra.xml"))
        image_path = os.path.join(self.IMAGES_TEST_FOLDER, "hnEVsPyTxnbJuBra.jpg")
        self.pdf_b.add_heading("OFP", font_size=30)
        starting_text = self.pdf_b.height * 0.8
        self.pdf_b.leading = 5 * mm
        self.pdf_b.add_text("signatur: test", text_position_y=starting_text, font_size=20)
        self.pdf_b.add_text("owner: thiago", font_size=20)

        self.pdf_b.next_page()
        self.pdf_b.add_searchable_image(image_path, ocr_data=ocr_data, text_only=True, draw_box=False,
                                        scale=.5)

        # create a new page
        self.pdf_b.next_page()

        # add another image
        ocr_data = OcrDataParse.parse_alto_xml(os.path.join(self.OCR_TEST_FOLDER, "BXZmvQxPXwTvmPJT.xml"))
        image_path = os.path.join(self.IMAGES_TEST_FOLDER, "BXZmvQxPXwTvmPJT.jpg")
        self.pdf_b.add_searchable_image(image_path, ocr_data=ocr_data, text_only=False, draw_box=False,
                                        scale=.5)

        self.pdf_b.save()

        self.assertTrue(os.path.exists(self.pdf_path))


if __name__ == '__main__':
    unittest.main()
