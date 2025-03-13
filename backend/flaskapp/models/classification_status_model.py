from __future__ import annotations
from enum import Enum

from sqlalchemy import func

from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class ClassificationStatus(Enum):
    OPEN = "Offen"
    CLOSED = "Abgeschlossen"
    WORKING = "In Bearbeitung"


class ClassificationStatusModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_CLASSIFICATION_STATUS

    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"), primary_key=True)
    search_category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"), primary_key=True)
    status = db.Column(db.Enum(ClassificationStatus))
    number_of_pages_classified = db.Column(db.Integer())
    has_ownership: bool = db.Column(db.Boolean, default=False)
    has_location: bool = db.Column(db.Boolean, default=False)

    def __repr__(self):
        atr = [f"{c.name}={getattr(self, c.name)}" for c in ClassificationStatusModel.__table__.columns]
        return f"{type(self).__name__}({', '.join(atr)})"

    def __eq__(self, other: ClassificationStatusModel):
        return self.digitalisat_id == other.digitalisat_id and self.search_category_id == other.search_category_id

    def __ne__(self, other):
        return self.digitalisat_id != other.digitalisat_id or self.search_category_id != other.search_category_id

    def to_dict(self):
        dto = dict()
        dto["digitalisatId"] = self.digitalisat_id
        dto["searchCategoryId"] = self.search_category_id
        dto["status"] = self.status.name
        dto["statusValue"] = self.status.value
        dto["numberOfPagesClassified"] = self.number_of_pages_classified
        dto["hasOwnership"] = self.has_ownership
        dto["hasLocation"] = self.has_location
        return dto

    @staticmethod
    def number_of_images_in_digitalisat_and_classification(digitalisat_id: str, category_id: str) -> int:
        """
        Gets the number of images that belong to this digitalisat and category.

        :param digitalisat_id: The digitalisat id
        :param category_id: The search category id
        :return: The number of images within this category and digitalisat.
        """
        from flaskapp.models import DigitalisatImageModel
        from flaskapp.models import ImageClassificationModel
        query_to_join = DigitalisatImageModel.query.session.query(func.count(DigitalisatImageModel.id)).filter(*[
            DigitalisatImageModel.digitalisat_id == digitalisat_id])
        query = query_to_join.join(ImageClassificationModel).filter(
            *[ImageClassificationModel.digitalisat_image_id == DigitalisatImageModel.id,
              ImageClassificationModel.search_category_id == category_id])
        return query.scalar()

    @classmethod
    def open_digitalisate_in_category(cls, category_id: str = None):
        """
        Gets all digitalisate with open state either in a given category or in all categories.

        :param category_id: The search category id
        :return: The number of images within this category and digitalisat.
        """
        from flaskapp.models import DigitalisatModel

        filters = [cls.status == ClassificationStatus.OPEN]
        if category_id:
            filters.append(cls.search_category_id == category_id)

        query = DigitalisatModel.query.filter(*[DigitalisatModel.id == cls.digitalisat_id]).distinct()
        query = query.join(cls).filter(*filters)
        entities: DigitalisatModel = query.all()
        return entities
