import os

from datetime import datetime

from sqlalchemy import func


from flaskapp import db
from flaskapp.models import BaseModel, TableNames, DigitalisatImageModel
from flaskapp.utils import TSVectorType


class DigitalisatImageOcrModel(db.Model, BaseModel):

    LANGUAGE = 'german'
    __tablename__ = TableNames.T_DIGITALISAT_IMAGE_OCR

    digitalisat_image_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT_IMAGE + ".id"),
                                     primary_key=True)
    ocr_text = db.Column(db.String())
    search_vector = db.Column(TSVectorType())
    create_date = db.Column(db.Date())

    @classmethod
    def create(cls, digitalisat_image_id: str, ocr_text: str):
        model = cls()
        model.digitalisat_image_id = digitalisat_image_id
        model.ocr_text = ocr_text
        model.search_vector = func.to_tsvector(cls.LANGUAGE, func.coalesce(ocr_text, ""))
        model.create_date = datetime.now().date()
        return model

    def update_ocr_text(self, ocr_text):
        self.ocr_text = ocr_text
        self.search_vector = func.to_tsvector(self.LANGUAGE, func.coalesce(ocr_text, ""))
        return self.save()

    def __repr__(self):
        atr = [f"{c.name}={getattr(self, c.name)}" for c in DigitalisatImageOcrModel.__table__.columns]
        return f"{type(self).__name__}({', '.join(atr)})"

    def get_ocr_files(self):
        """
        Gets the alto xml and json file path.

        :return: A tuple of strings with the file path for the alto and the json data if exists,
            otherwise it returns a tuple of None.
        """
        image: DigitalisatImageModel = self.digitalisat_image  # backref
        return image.get_ocr_files()
