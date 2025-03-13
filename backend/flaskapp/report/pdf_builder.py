import os
from io import BytesIO
from typing import Tuple, Union

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle


class PdfBuilder:

    # STANDARD_FONT = "Times-Roman"

    def __init__(self, pdf_path: str,  pagesize=A4):
        self.pdf_path = pdf_path
        self.canvas = Canvas(self.pdf_path, pagesize=pagesize)
        self.standard_font = "Times-Roman"

        self.width, self.height = pagesize
        self.margin = 10.
        self.leading = 2*mm
        self.__current_y_location = self.height

    def add_heading(self, text: str, color="black", **kwargs):
        """
        Add a Heading at the top of the page.

        :param text: The text to be written at the heading.

        :param color: The text color.

        :keyword font_size: The size of the font. Default=16

        :keyword leading:
        """
        font_name = "Times-Bold"
        font_size = kwargs.get("font_size", 16)
        leading = kwargs.get("leading", 16*mm)
        text_position_x = 0
        text_width = stringWidth(text, font_name, font_size)
        if self.width > text_width:
            text_position_x = round((self.width - text_width) / 2)
        text_position_y = self.get_end_of_text() - leading

        self.add_text(text, text_position_x=text_position_x, text_position_y=text_position_y,
                      font_size=font_size, font_type=font_name, color=color)

    def _get_text_position_x(self, text: str, font_type: str, font_size: int, position="centre"):
        """
        Gets the y position for this text relative to the position.

        :param text: The text to be written at the heading.
        :param font_type: The name of the font.
        :param font_size: The size of the font.
        :param position: The horizontal position (values: centre, left, right.
        """
        text_width = stringWidth(text, font_type, font_size)
        if position == "left":
            if self.width > text_width:
                return round(self.width/4 - text_width/2)
        elif position == "right":
            if self.width > text_width:
                return round(self.width/4 + self.width/2 - text_width/2)
        else:
            if self.width > text_width:
                return round(self.width/2 - text_width/2)

    def add_table(self, data, position_x=0, position_y=0, width=0, height=0,
                  font_size=12, font_type=None, color="black"):
        font_type = font_type if font_type else self.standard_font
        table = Table(data)
        table.setStyle(
            TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), color), ('FONT', (0, 0), (-1, -1), font_type),
                        ('FONTSIZE', (0, 0), (-1, -1), font_size)]))
        table.wrapOn(self.canvas, width, height)
        table.drawOn(self.canvas, position_x, position_y)
        self.__current_y_location -= height + self.margin

    def add_text(self, text: str, text_position_x=0, text_position_y=0,
                 font_size=12, font_type=None, color="black", leading=True):
        """
        Add a text to the PDF with the given parameters.

        :param text: The text to be added.

        :param text_position_x: The x text position. If default=0 the text will be added
            to the page margin.

        :param text_position_y: The y text position. If default=0 the text will be
            added to the next line.

        :param font_size: The size of the font. Default=12

        :param font_type: The type of the font.

        :param color: The color of the font.

        :param leading: Default=True. If False the leading will be removed from text_position_y.

        :return:
        """
        font_type = font_type if font_type else self.standard_font
        text = text.replace("\n", "<br/>")
        text_position_x = text_position_x if text_position_x != 0 else self.margin
        text_position_y = text_position_y if text_position_y != 0 else self.get_end_of_text()
        if not leading:
            text_position_y += self.leading  # remove leading

        st = ParagraphStyle(name='Justify', alignment=TA_JUSTIFY,
                            fontSize=font_size, fontName=font_type, textColor=color)
        p = Paragraph(text, style=st)
        justify_width = self.width - 2 * self.margin
        justify_height = self.height - 2 * self.margin
        w, h = p.wrap(justify_width - text_position_x, justify_height - text_position_y)
        p.drawOn(self.canvas, text_position_x, text_position_y - h)
        self.__current_y_location = round(text_position_y - p.height - self.leading)
        return stringWidth(text, font_type, font_size), h

    def next_page(self):
        """
        Close the current page and start on a new page.

        :return:
        """
        self.canvas.showPage()

    def add_image_to_new_page(self, image_path, label=""):
        """

        :param image_path:
        :param label:
        :return:
        """
        width = self.width - 2 * self.margin
        height = self.height - 4 * self.margin
        try:
            self.next_page()
            self.add_image_at(image_path, caption=label, position_x=self.width*0.5, position_y=self.height*0.5,
                              width=width, height=height, caption_x=self.margin, anchor="c")
        except FileNotFoundError:
            # TODO deal with images that were not found.
            pass

    def add_image_at(self, image_path: str, caption: str, position_x, position_y, **kwargs):
        """
        Add image at the given location.

        :param image_path: The image path.

        :param caption: A caption for this image.

        :param position_x: The x position where the image should be added

        :param position_y: The y position where the image should be added.

        :param kwargs: Possible kwargs

        :keyword width: The desired image's width. The aspect-rate will be always preserved, therefore width
            may not be exactly the given value.
        :keyword height: The desired image's height. The aspect-rate will be always preserved, therefore height
            may not be exactly the given value.

        :keyword anchor: The default value is 'nw' for 'upper-left corner'. Possible values are nw n ne w c e sw s se

        :keyword font_size: The size of the font used for the caption. Default=8.

        :keyword font_type:  The type of the font. Default=standard_font

        :exception FileNotFoundError

        :return:
        """
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"The file at {image_path} doesn't exits.")

        width = kwargs.get("width", None)
        height = kwargs.get("height", None)
        font_size = kwargs.get("font_size", 8)
        font_type = kwargs.get("font_type", self.standard_font)
        anchor = kwargs.get("anchor", 'nw')

        im_w, im_h = self.canvas.drawImage(image_path, x=position_x, y=position_y, width=width, height=height,
                                           preserveAspectRatio=True, anchor=anchor, anchorAtXY=True)
        if caption:
            r = float(im_h)/float(im_w)  # image aspect ratio. im_h and im_w are height and width of the original image.
            resize_h = height if r > 1. else width * r
            resize_w = width if r < 1. else height / r
            x, y = self.get_optimal_caption_position(position_x, position_y, resize_w, resize_h, anchor)
            self.add_text(caption, text_position_x=x, text_position_y=y, font_size=font_size, font_type=font_type)

    @staticmethod
    def get_optimal_caption_position(x, y, w, h, anchor):
        """
        Computes the best position to add the image label based on the used anchor.
        :param x:
        :param y:
        :param w: The
        :param h:
        :param anchor:
        :return:
        """

        if anchor == "c":
            return x - w*0.5, y - h*0.5
        elif anchor == "nw":
            return x, y - h
        elif anchor == "n":
            return x - w*0.5, y - h
        elif anchor == "ne":
            return x - w, y - h
        elif anchor == "w":
            return x, y - h*0.5
        elif anchor == "e":
            return x - w, y - h*0.5
        elif anchor == "sw":
            return x, y
        elif anchor == "s":
            return x - w*0.5, y
        elif anchor == "se":
            return x - w, y
        else:
            return 0, 0

    def add_link(self, url, position_x, position_y, annotation=None, font_size=8, color="blue"):

        annotation = annotation if annotation else url
        w, h = self.add_text(annotation, text_position_x=position_x, text_position_y=position_y,
                              color=color, font_size=font_size)
        r1 = (position_x, position_y - h, position_x + w, position_y)  # this is x1,y1,x2,y2
        self.canvas.linkURL(url, r1, relative=1, thickness=0)

    def get_end_of_text(self) -> int:
        """
        Get the y position where the text ends + leading.

        :return: The y position where the text ends + leading.
        """
        return self.__current_y_location

    def fit_text_to_box(self, text, rect: Tuple[float, float, float, float], draw_box=False):
        """
        Fix the given text to the given box

        :param text: A string
        :param rect: Expected a Tuple with 4 positions (x, y, width, height)
        :param draw_box: If true it will draw the box around the text.
        :return:
        """
        # if text is empty abort
        if not text:
            return
        x, y, w, h = rect
        fs = h
        fw = self.canvas.stringWidth(text, fontName=self.standard_font, fontSize=fs)
        tries = 0
        outer_bound = 0
        inner_bound = 0
        while abs(w - fw) > 1:
            if fw > w:
                fs -= 0.5
                outer_bound = 1
            else:
                fs += 0.5
                inner_bound = 1

            if fs <= 1 or outer_bound*inner_bound > 0 or tries > 1000:
                # print(text, fs, outer_bound * inner_bound, w - fw, tries)
                # print("break for", text, fs, h, abs(w - fw), tries)
                break

            fw = self.canvas.stringWidth(text, fontName=self.standard_font, fontSize=fs)
            tries += 1

        if fw >= w:  # ensure is inside the box.
            fs -= 1

        if fs > 1.5*h:  # rescale based in height, for font size that are 50% bigger than height decrease size by 20%.
            fs -= 0.2*fs

        empty_vertical_space = h - fs  # assumes text height is equal to its font size.
        text_base_line = y
        if empty_vertical_space > 0:
            text_base_line += empty_vertical_space/2.  # adjust font to fill half of the empty space on vertical

        self.canvas.setFont(self.standard_font, fs)
        self.canvas.drawString(x, text_base_line, text)
        if draw_box:
            self.canvas.rect(x, y, w, h)

    @staticmethod
    def convert_bytes_to_image_reader(img: BytesIO):
        return ImageReader(img)

    def fit_image_to_page(self, image: Union[BytesIO, str]):
        if isinstance(image, BytesIO):
            image = self.convert_bytes_to_image_reader(image)
        self.canvas.drawImage(image, x=0, y=0, width=self.width, height=self.height,
                              preserveAspectRatio=True, anchor="sw", anchorAtXY=True)

        if isinstance(image, ImageReader) and isinstance(image.fileName, BytesIO):
            image.fileName.close()

    def save(self):
        self.canvas.save()
