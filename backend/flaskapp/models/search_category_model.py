from __future__ import annotations

from typing import Union, List

from flaskapp import db
from flaskapp.models import TableNames, BaseModel, Relationship, SearchTermModel, BlacklistTermModel, \
    NonRelevantTermModel, DigitalisatClassificationLockModel


class SearchCategoryModel(db.Model, BaseModel):

    DEFAULT_CATEGORY_NAME = "Unclassified"

    __tablename__ = TableNames.T_SEARCH_CATEGORY

    id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    order = db.Column(db.Integer, default=lambda: SearchCategoryModel.next_order())

    search_terms = db.relationship(Relationship.SEARCH_TERM,
                                   backref="search_category",
                                   cascade="all, delete-orphan", lazy=True)
    blacklist_terms = db.relationship(Relationship.BLACKLIST_TERM,
                                      backref="search_category",
                                      cascade="all, delete-orphan", lazy=True)

    non_relevant_terms = db.relationship(Relationship.NON_RELEVANT_TERM,
                                         backref="search_category",
                                         cascade="all, delete-orphan", lazy=True)

    classifications_lock = db.relationship(
        Relationship.DIGITALISAT_CLASSIFICATION_LOCK, backref="search_category", cascade="save-update,merge, delete",
        lazy=True)

    classifications_status = db.relationship(Relationship.CLASSIFICATION_STATUS, backref="search_category",
                                             cascade="save-update,merge, delete",
                                             lazy=True)
    image_classification = db.relationship(Relationship.IMAGE_CLASSIFICATION, backref="search_category",
                                           cascade="save-update, merge, delete", lazy=True)

    vorgang = db.relationship(Relationship.VORGANG, backref="search_category", cascade="save-update, merge, delete",
                              lazy=True)

    def to_dict(self):
        """
        Convert SearchCategoryModel into a dictionary, this way we can convert it to a JSON response.

        :return: A clean dictionary form of this model.
        """
        # convert columns to dict
        dict_representation = super().to_dict()
        # dict_representation["searchTerms"] = self.get_search_terms()
        dict_representation["searchTerms"] = [search_term.to_dict() for search_term in self.search_terms]
        dict_representation["blacklist"] = [blt.to_dict() for blt in self.blacklist_terms]
        dict_representation["ignoreList"] = [nrt.to_dict() for nrt in self.non_relevant_terms]

        return dict_representation

    def get_all_search_terms(self):
        return [st.search_value for st in self.search_terms]

    def delete_search_terms(self):
        SearchTermModel.bulk_delete(filters=[SearchTermModel.category_id == self.id])

    def get_all_blacklist_terms(self):
        return [blt.value for blt in self.blacklist_terms]

    def delete_blacklist_terms(self):
        BlacklistTermModel.bulk_delete(filters=[BlacklistTermModel.category_id == self.id])

    def get_all_non_relevant_terms(self):
        return [nrt.value for nrt in self.non_relevant_terms]

    def delete_non_relevant_terms(self):
        NonRelevantTermModel.bulk_delete(filters=[NonRelevantTermModel.category_id == self.id])

    @classmethod
    def next_order(cls) -> int:
        return cls.total() + 1

    @classmethod
    def from_dict(cls, dto: dict):
        category_model: SearchCategoryModel = super().from_dict(dto)
        category_model.name = dto.get("name", None)
        category_model.description = dto.get("description", None)
        search_term_items = dto.get("searchTerms", [])
        category_model.search_terms = [SearchTermModel.from_dict(item) for item in search_term_items]
        category_model.blacklist_terms = [BlacklistTermModel.from_dict(item) for item in dto.get("blacklist", [])]
        category_model.non_relevant_terms = [NonRelevantTermModel.from_dict(item) for item in dto.get("ignoreList", [])]

        return category_model

    @classmethod
    def get_categories_without_default(cls) -> List[SearchCategoryModel]:
        """
        Get all Categories without the default value for unknown classification.

        :return:
        """
        return cls.find_by_filter(filters=[cls.name != cls.DEFAULT_CATEGORY_NAME])

    @classmethod
    def get_unknown(cls) -> Union[SearchCategoryModel, None]:
        """
        This is a default value for unknown classification.

        :return:
        """
        return cls.find_by(name=cls.DEFAULT_CATEGORY_NAME)
