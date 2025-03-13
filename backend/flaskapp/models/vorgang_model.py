from typing import List

from flaskapp import db
from flaskapp.models import BaseModel, TableNames, Relationship
from flaskapp.utils import DateUtils


class VorgangImagesModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_VORGANG_IMAGES

    vorgang_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_VORGANG + ".id"), primary_key=True)
    digitalisat_image_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT_IMAGE + ".id"),
                                     primary_key=True)


class VorgangModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_VORGANG

    id = db.Column(db.String(16), primary_key=True)
    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"))
    search_category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"))
    vorgang_order = db.Column(db.Integer())
    create_date = db.Column(db.Date())

    vorgang_images = db.relationship(Relationship.VORGANG_IMAGES, backref="vorgang",
                                     cascade="save-update, merge, delete", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "createDate": DateUtils.convert_date_to_german_string(self.create_date),
            "digitalisat": self.digitalisat.to_dict(), "searchCategory": self.search_category.to_dict(),
        }

    @property
    def name(self):
        from flaskapp.models import SearchCategoryModel

        search_category_model: SearchCategoryModel = self.search_category  # back ref
        return f"{search_category_model.name} [{self.vorgang_order:03d}/{self.create_date:%y}]"

    @classmethod
    def get_next_order(cls, category_id):
        model: cls = cls.find_by(search_category_id=category_id, order_by=cls.vorgang_order.desc(), get_first=True)
        if model:
            return model.vorgang_order + 1
        return 1

    def delete_vorgang_images(self):
        for entity in self.vorgang_images:
            entity.delete()

    def get_images_ids(self):
        """ Get a list of digitalisat images ids for this Vorgang."""
        return [entity.digitalisat_image_id for entity in self.vorgang_images]

    @staticmethod
    def __sort_image_by_order(image_model):
        return image_model.image_order

    def get_images(self):
        """ Get a list of digitalisat images for this Vorgang."""
        # entity.digitalisat_image is backref
        images = [entity.digitalisat_image for entity in self.vorgang_images]
        images.sort(key=self.__sort_image_by_order)
        return images

    def has_image(self, digitalisat_image_id):
        return digitalisat_image_id in self.get_images_ids()

    def add_digitalisat_image(self, digitalisat_image_id: str):
        """
        Add image to this vorgang.

        Important: This will not be added to the database until vorgang is saved.

        :param digitalisat_image_id: The DigitalisatImage id.

        :return:
        """
        if not self.has_image(digitalisat_image_id):
            vorgang_images = VorgangImagesModel(vorgang_id=self.id, digitalisat_image_id=digitalisat_image_id)
            self.vorgang_images.append(vorgang_images)

    def add_digitalisat_images(self, digitalisat_images_ids: List[str]):
        """
        Add images to this vorgang.

        Important: This will not be added to the database until vorgang is saved.

        :param digitalisat_images_ids: A list of DigitalisatImage ids.
        :return:
        """
        for digitalisat_image_id in digitalisat_images_ids:
            self.add_digitalisat_image(digitalisat_image_id)
