import json

from flaskapp import db
from flaskapp.models import BaseModel, TableNames


class ImageClassificationModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_IMAGE_CLASSIFICATION
    digitalisat_image_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT_IMAGE + ".id"),
                                     primary_key=True)
    search_category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"), primary_key=True)
    found_terms = db.Column(db.JSON(), nullable=False)

    @classmethod
    def get_found_terms(cls, digitalisat_image_id, category_id):
        model = cls.find_by(
            digitalisat_image_id=digitalisat_image_id,
            search_category_id=category_id,
            get_first=True
        )
        if model and model.found_terms:
            return json.loads(model.found_terms)
        return []

    @classmethod
    def delete_images_from_classification(cls, digitalisat_id: str, search_category_id: str) -> bool:
        """
        Delete all digitalisat's images from the given classification.
        :param digitalisat_id: The
        :param search_category_id:
        :return:
        """

        from flaskapp.models import DigitalisatImageModel

        images_ids_query = cls.query.with_entities(
            cls.digitalisat_image_id).distinct().join(DigitalisatImageModel).\
            filter(*[DigitalisatImageModel.digitalisat_id == digitalisat_id])

        filters = [
            cls.search_category_id == search_category_id,
            cls.digitalisat_image_id.in_(images_ids_query)
        ]

        return cls.bulk_delete(filters=filters)


# This event is called every time a ImageClassificationModel instance is deleted.
# @event.listens_for(ImageClassificationModel, 'after_delete')
# def receive_after_delete(mapper, connection, target: ImageClassificationModel):
#     digitalisat_image_id
#     pass
