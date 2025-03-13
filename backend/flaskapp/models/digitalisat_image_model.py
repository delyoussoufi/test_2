import json
import os
from typing import Union, Tuple, List

from sqlalchemy import func

from flaskapp import db
from flaskapp.classification.data_structure import SearchTerm
from flaskapp.models import BaseModel, TableNames, DigitalisatModel, Relationship, ImageClassificationModel
from flaskapp.utils import parse_to_ts_query_string


class DigitalisatImageModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_DIGITALISAT_IMAGE

    id = db.Column(db.String(16), primary_key=True)
    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"))
    name = db.Column(db.String(400), nullable=False)
    image_order = db.Column(db.Integer(), nullable=False)
    sha1 = db.Column(db.String(40), nullable=False)
    image_size = db.Column(db.Float(), nullable=False)

    ocr_data = db.relationship(Relationship.DIGITALISAT_IMAGE_OCR, uselist=False, backref="digitalisat_image",
                               cascade="save-update, merge, delete", lazy=True)
    vorgang_images = db.relationship(Relationship.VORGANG_IMAGES, backref="digitalisat_image",
                                     cascade="save-update, merge, delete", lazy=True)
    image_classifications = db.relationship(Relationship.IMAGE_CLASSIFICATION,
                                            backref="digitalisat_image",
                                            cascade="save-update, merge, delete",
                                            lazy=True)

    def __repr__(self):
        atr = (f"{key}={value}" for key, value in self.to_dict().items())
        return f"{type(self).__name__}({', '.join(atr)})"

    def to_dict(self):
        dto = dict()
        dto["id"] = self.id
        dto["digitalisatId"] = self.digitalisat_id
        dto["name"] = self.alias_name
        dto["order"] = self.image_order
        dto["sha1"] = self.sha1
        dto["size"] = self.image_size / (1024*1024)  # MB
        dto["categoriesIds"] = [ics.search_category_id for ics in self.image_classifications]
        return dto

    def add_classification(self, category_id: str, found_terms: List[SearchTerm]):
        """
        Add classification terms to this image if found_terms is not empty. If the classification already
        exists for this digitalisat_image, then it just update the found_terms.

        !Important you must save() the entity for this to be added.

        :param category_id: The id of the category to be found.
        :param found_terms: A list of SearchTerm
        :return:
        """
        from flaskapp.models.image_classification_model import ImageClassificationModel

        if found_terms:
            icm = next((icm for icm in self.image_classifications
                        if icm.search_category_id == category_id and icm.digitalisat_image_id == self.id), None)

            json_terms = json.dumps([r.to_dict() for r in found_terms], indent=0)
            if icm:
                # if found in the list just update found terms.
                icm.found_terms = json_terms
            else:
                # if not found in the list append a new item.
                icm = ImageClassificationModel(digitalisat_image_id=self.id, search_category_id=category_id)
                icm.found_terms = json_terms
                self.image_classifications.append(icm)

    def delete_image_classification(self, search_category_id: str = None):
        """
        This will delete classification from this image at the database. If no search_category_id is given
        then all classification from this image will be removed.

        :param search_category_id: If given, only classification associated with this category will be deleted.
        """
        # creates an iterator
        ic_iter = (ic for ic in self.image_classifications if ic.search_category_id == search_category_id or
                   search_category_id is None)
        for ic in ic_iter:
            ic.delete()

    @property
    def image_path(self):
        digitalisat_model: DigitalisatModel = self.digitalisat  # get it via backref.
        image_path = os.path.join(digitalisat_model.dir_path, self.name)
        return image_path

    @property
    def alias_name(self):
        return f"blha{self.name.split('_blha')[-1]}"

    @classmethod
    def create_from_digi_image(cls, digi_image: dict):
        """
        Create an entity from from digiproduction. You must call the
        save method to add it to the database.

        :param digi_image: A dictionary representation of digiproduction digitalisat_image.
        :return: An entity of this model.
        """
        model = cls.from_dict(digi_image)
        model.digitalisat_id = digi_image.get("digitalisatId", None)
        model.image_order = digi_image.get("order", 0)
        model.sha1 = None
        model.image_size = 0
        return model

    def get_ocr_files(self) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        Gets the alto xml and json file path.

        :return: A tuple of strings with the file path for the alto and the json data if exists,
            otherwise it returns a tuple of None.
        """
        digitalisat = self.digitalisat  # backref
        return digitalisat.get_ocr_files(self.id)

    @classmethod
    def find_images_with_digitalisat_and_classification(cls, digitalisat_id: str, category_id: str,
                                                        text_search: str = None) -> List['DigitalisatImageModel']:

        filters = [cls.digitalisat_id == digitalisat_id, ImageClassificationModel.search_category_id == category_id]
        query = cls.query.join(ImageClassificationModel)
        if text_search:
            from flaskapp.models import DigitalisatImageOcrModel
            text_search = parse_to_ts_query_string(text_search)
            tsquery_func = func.to_tsquery(DigitalisatImageOcrModel.LANGUAGE, text_search)
            filters.append(DigitalisatImageOcrModel.search_vector.op('@@')(tsquery_func))
            query = query.join(DigitalisatImageOcrModel)

        query = query.filter(*filters).order_by(cls.image_order)
        return query.all()

    @classmethod
    def find_images_with_digitalisat_and_text(cls, digitalisat_id: str, text_search: str):
        from flaskapp.models import DigitalisatImageOcrModel

        text_search = parse_to_ts_query_string(text_search)
        tsquery_func = func.to_tsquery(DigitalisatImageOcrModel.LANGUAGE, text_search)
        filters = [cls.digitalisat_id.__eq__(digitalisat_id),
                   DigitalisatImageOcrModel.search_vector.op('@@')(tsquery_func)]
        query = cls.query.join(DigitalisatImageOcrModel, isouter=True).filter(*filters).order_by(cls.image_order)
        return query.all()
