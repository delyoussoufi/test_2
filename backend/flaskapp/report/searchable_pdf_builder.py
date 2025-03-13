from io import BytesIO

from PIL import Image
from PIL.Image import Resampling
from PIL.JpegImagePlugin import JpegImageFile

from reportlab.lib.pagesizes import A4

from flaskapp.report import PdfBuilder
from flaskapp.structures import OcrData


class SearchablePdfBuilder(PdfBuilder):

    def __init__(self, pdf_path: str, pagesize=A4):
        super().__init__(pdf_path, pagesize=pagesize)
        self.standard_font = "Courier"  # change standard font.

    def set_size(self, size):
        self.width, self.height = size
        self.canvas.setPageSize(size)

    def add_searchable_image(self, image_path: str, ocr_data: OcrData = None, text_only=False,
                             draw_box=False, scale=1.):

        with Image.open(image_path, mode='r') as img:
            img: JpegImageFile
            # resize image based on scale
            i_width, i_height = round(img.size[0] * scale), round(img.size[1] * scale)
            output_image = img.resize((i_width, i_height), Resampling.LANCZOS)

            with BytesIO() as output_io:
                # save to a byte array
                output_image.save(output_io, "JPEG")
                pagesize = output_image.size
                output_image.close()  # can close at this point

                original_size = self.width, self.height
                self.set_size(pagesize)

                if ocr_data:
                    for word in ocr_data.words:
                        p_text, rec = word.text, word.box * scale
                        w = rec.xf - rec.x0
                        h = rec.yf - rec.y0
                        self.fit_text_to_box(p_text, (rec.x0, self.height - rec.yf, w, h), draw_box=draw_box)

                if not text_only:
                    self.fit_image_to_page(output_io)

        # keep the width and height as the original
        self.width, self.height = original_size

