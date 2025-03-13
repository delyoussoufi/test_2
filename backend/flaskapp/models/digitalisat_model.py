from __future__ import annotations

import os
from builtins import filter
from datetime import datetime
from operator import or_
from typing import List, Union, Tuple, Optional

import werkzeug
from sqlalchemy import func, cast, desc, asc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import undefer

from flaskapp import db, app_logger
from flaskapp.config import active_config
from flaskapp.http_util.mapper import map_to_ts_style
from flaskapp.models import BaseModel, TableNames, Relationship, TargetFolderModel, ClassificationStatusModel, \
    ClassificationStatus, DigitalisatCommentsModel
from flaskapp.models.enums import DigitalisatStatus
from flaskapp.search.digitalisat_search import DigitalisatSearch
from flaskapp.structures.structures import SearchDefault, SearchResult
from flaskapp.utils import DateUtils, parse_to_ts_query_string, StringUtils


class DigitalisatModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_DIGITALISAT

    id = db.Column(db.String(16), primary_key=True)
    scope_id = db.Column(db.String(20))
    folder_name = db.Column(db.String(400))
    signature = db.Column(db.String(200))
    target_folder_id = db.Column(db.String(), db.ForeignKey(TableNames.T_TARGET_FOLDERS + ".id"))
    sub_folder = db.Column(db.Integer())
    archivalien_art_id = db.Column(db.String(16))
    expected_images = db.Column(db.Integer())
    status = db.Column(db.Enum(DigitalisatStatus))
    create_date = db.Column(db.Date())
    delete_date = db.Column(db.Date())

    signature_number = db.deferred(cast(func.regexp_replace(
        signature, StringUtils.EXTRACT_SIGNATURE_NUMBER_PATTERN, "", "gi"), db.Integer).label("signature_number"))

    scope_data = db.relationship(Relationship.SCOPE_DATA, backref="digitalisat", uselist=False,
                                 cascade="save-update, merge, delete", lazy=True)
    # lazy="dynamic" will not load the object automatically.
    digitalisat_images = db.relationship(Relationship.DIGITALISAT_IMAGE, backref="digitalisat",
                                         cascade="save-update, merge, delete", lazy=True)

    classifications_status = db.relationship(Relationship.CLASSIFICATION_STATUS,
                                             backref="digitalisat",
                                             cascade="save-update,merge, delete",
                                             lazy=True)

    classifications_lock = db.relationship(
        Relationship.DIGITALISAT_CLASSIFICATION_LOCK, backref="digitalisat", cascade="save-update,merge, delete",
        lazy=True)

    digitalisat_comments = db.relationship(Relationship.DIGITALISAT_COMMENTS,
                                           backref="digitalisat",
                                           cascade="save-update, merge, delete",
                                           lazy=True)
    vorgang = db.relationship(Relationship.VORGANG, backref="digitalisat", cascade="save-update, merge, delete",
                              lazy=True)

    def __repr__(self):
        atr = (f"{key}={value}" for key, value in self.to_dict().items())
        return f"{type(self).__name__}({', '.join(atr)})"

    @map_to_ts_style()
    def to_dict(self):
        dto = super().to_dict()
        dto["statusValue"] = self.status.value
        dto["status"] = self.status.name
        dto["numberOfImages"] = self.number_of_images()
        dto["createDate"] = DateUtils.convert_date_to_german_string(self.create_date)
        dto["deleteDate"] = DateUtils.convert_date_to_german_string(self.delete_date)
        dto["scopeData"] = self.scope_data.to_dict() if self.scope_data else None
        dto["classificationStatus"] = [cs_model.to_dict() for cs_model in self.classifications_status]
        # noinspection PyUnresolvedReferences
        dto["lockedCategories"] = [dc_locked.search_category.to_dict() for dc_locked in self.classifications_lock]

        # change expectedImages based on query
        text_filter = getattr(self, "text_filter", None)
        if text_filter:
            dto["expectedImages"] = self.number_of_images(text_filter, getattr(self, "category_id", None))
        return dto

    @property
    def dir_path(self) -> str:
        # self.target_folder is from backref of TargetFolderModel
        # noinspection PyUnresolvedReferences
        dir_path = os.path.join(self.target_folder.path, str(self.sub_folder), self.folder_name)
        return str(dir_path)

    @property
    def ocr_dir(self):
        ocr_dir = os.path.join(self.dir_path, "OCR")
        if not os.path.isdir(ocr_dir):
            os.mkdir(ocr_dir)

        return ocr_dir

    @classmethod
    def digi_digitalisat_has_ocr(cls, digi_digitalisat: dict):
        ocr_status: Optional[dict] = digi_digitalisat.get("ocrStatus", None)
        if ocr_status:
            return ocr_status.get("status", None) == "FINISHED"
        else:
            return False

    @classmethod
    def create_from_digi_digitalisat(cls, digi_digitalisat: dict) -> Tuple[DigitalisatModel, bool]:
        """
        Create an entity from digiproduction. This method
        will also create the digitalisat folder if the id doesn't exist. You must call the
        save method to add it to the database. If a digitalisat already exits in the dms then it
        just return the existing digitalisat.

        :param digi_digitalisat: A dictionary representation of digiproduction digitalisat.
        :return: An a tuple (entity, new), where entity is an object from this model and new is a bool
            saying either object is new or not.
        """
        model = cls.from_dict(digi_digitalisat)
        model.scope_id = digi_digitalisat.get("scopeId", None)
        model.archivalien_art_id = digi_digitalisat.get("archivalienArtId", None)
        model.expected_images = digi_digitalisat.get("numberOfImages", 0)
        model.folder_name = digi_digitalisat.get("folderName", None)
        model.create_date = datetime.today().date()

        # uses ID or Signature to check if a digitalisat already exists
        existent_model: List[DigitalisatModel] = cls.find_by_filter(
            filters=
            [
                cls.id == model.id,
                cls.signature == model.signature
            ],
            use_or=True
        )

        if not existent_model:
            model.status = DigitalisatStatus.IDLE
            target_folder: TargetFolderModel = TargetFolderModel.find_active_target_folder()
            model.target_folder_id = target_folder.id
            sub_dir: str = target_folder.create_sub_folder()
            model.sub_folder = int(os.path.basename(sub_dir)) if sub_dir else None
            digitalisat_folder = os.path.join(str(sub_dir), str(model.folder_name))
            if not os.path.exists(digitalisat_folder):
                os.mkdir(digitalisat_folder)
            model.add_scope_data()
            return model, True
        else:
            return existent_model[0], False

    def add_scope_data(self):
        from flaskapp.models import ScopeDataModel
        from flaskapp.services.scope_service import ScopeService, DigitalisatScopeInfo
        if not self.scope_data:

            results = ScopeService(active_config).get_gsft_obj_dtl(int(self.scope_id))

            dsi = DigitalisatScopeInfo(self.scope_id, self.signature)
            dsi.map_gsft_objs_dtl(results)

            scope_data = ScopeDataModel.from_digitalisat_scope_info(dsi)
            scope_data.digitalisat_id = self.id
            self.scope_data = scope_data

    def synchronize_scope_data(self):
        from flaskapp.services.scope_service import ScopeService, DigitalisatScopeInfo

        # if there is no scope data try to add.
        if not self.scope_data:
            self.add_scope_data()
            return

        results = ScopeService(active_config).get_gsft_obj_dtl(int(self.scope_id))

        try:
            if results:
                dsi = DigitalisatScopeInfo(self.scope_id, self.signature)
                dsi.map_gsft_objs_dtl(results)

                self.scope_data.map_values_from_digitalisat_scope_info(dsi)
                self.scope_data.save()
        except ValueError as e:
            app_logger.error(str(e))

    @classmethod
    def get_idles(cls):
        """
        Gets digitalisate with idl status. This will return a max number of 100 digitalisate.

        :return: A list of digitalisat with idle status.
        """
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.IDLE], page=1, per_page=100).items

    @classmethod
    def get_downloading_images_status(cls) -> List[DigitalisatModel]:
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.DOWNLOADING_IMAGES])

    @classmethod
    def get_running_ocr_status(cls) -> List[DigitalisatModel]:
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.RUNNING_OCR])

    @classmethod
    def get_downloaded_images_status(cls) -> List[DigitalisatModel]:
        """
       Gets digitalisate with downloaded status. This will return a max number of 100 digitalisate.

       :return: A list of digitalisat with downloaded status.
       """
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.IMAGES_DOWNLOADED],
                                  page=1, per_page=100).items

    @classmethod
    def get_ocr_finished_status(cls) -> List[DigitalisatModel]:
        """
       Gets digitalisate with ocr finished status. This will return a max number of 100 digitalisate.

       :return: A list of digitalisat with ocr finished status.
       """
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.OCR_FINISHED],
                                  page=1, per_page=100).items

    @classmethod
    def get_classifying_status(cls) -> List[DigitalisatModel]:
        """
       Gets digitalisate with classifying status. This will return a max number of 100 digitalisate.

       :return: A list of digitalisat with classifying status.
       """
        return cls.find_by_filter(filters=[cls.status == DigitalisatStatus.CLASSIFYING],
                                  page=1, per_page=100).items

    @classmethod
    def get_digitalisate_with_open_or_no_classification(cls, category_id: Optional[str] = None):

        sub_select = select(ClassificationStatusModel)
        if category_id:
            sub_select.where(ClassificationStatusModel.search_category_id == category_id)

        subquery = sub_select.subquery()

        filters = [
            cls.status == DigitalisatStatus.FINISHED,
            or_(
                subquery.c.status == ClassificationStatus.OPEN,
                # this can happen on join when digitalisate has no classification
                subquery.c.status.__eq__(None)
            ),
        ]

        stm = select(cls).distinct().outerjoin(subquery, subquery.c.digitalisat_id.__eq__(cls.id)).filter(*filters)
        return db.session.execute(stm).scalars().all()

        # ref code remove if all everything is okay. The sql select above should behavior in the same way as
        # the code below

        # models: List[cls] = cls.find_by_filter(filters=[cls.status == DigitalisatStatus.FINISHED])
        #
        # def classification_status_filter(dm: DigitalisatModel):
        #
        #     if not category_id:
        #         # all classifications need to be analysed if at least one has open status then return true or
        #         # if there is no classification (shouldn't happen)
        #         if len(dm.classifications_status) == 0:
        #             return True
        #         else:
        #             classifications_status = [cs for cs in dm.classifications_status
        #                                       if cs.status == ClassificationStatus.OPEN]
        #             return len(classifications_status) > 0
        #     else:
        #         # for single classification
        #         cs = dm.get_classification_status(category_id)
        #
        #         if not cs:
        #             return True
        #         elif cs.status == ClassificationStatus.OPEN:
        #             return True
        #         else:
        #             return False
        #
        # return list(filter(classification_status_filter, models))

    @classmethod
    def find_digitalisate_by_target_folder_id(cls, target_folder_id: str):
        """
        This will find all digitalisats with the targetfolder.

        :param target_folder_id: The id of the target folder
        :return: A list of DigitalisatModel or None.
        """
        return cls.find_by(target_folder_id=target_folder_id, delete_date=None, get_first=False)

    def number_of_images(self, text_filter: str = None, category_id: str = None) -> int:
        """
        Get the number of images that belong to this digitalisat.

        text_filter = A text query to filter images.
        category_id = A category id to filter images, only used if text_filter is also provide.

        :return: The number of images that belong to this digitalisat.
        """
        from flaskapp.models import DigitalisatImageModel, DigitalisatImageOcrModel, ImageClassificationModel

        filters = [DigitalisatImageModel.digitalisat_id.__eq__(self.id)]
        if text_filter:
            text_search = parse_to_ts_query_string(text_filter)
            tsquery_func = func.to_tsquery(DigitalisatImageOcrModel.LANGUAGE, text_search)
            filters.append(DigitalisatImageOcrModel.search_vector.op('@@')(tsquery_func))

            query = select(func.count(DigitalisatImageModel.id))\
                .join(DigitalisatImageOcrModel, isouter=True)

            if category_id:
                filters.append(ImageClassificationModel.search_category_id == category_id)
                query = query.join(ImageClassificationModel, isouter=True)

            return db.session.execute(query.filter(*filters)).scalar_one()

        return DigitalisatImageModel.total(filters=filters)

    def has_all_images(self) -> bool:
        return self.expected_images == len(self.digitalisat_images)

    def delete_classifications_status(self, search_category_ids: List[str] = None):
        """
        This will delete classifications_status from this digitalisat at the database. If
        search_category_ids is not given it will delete all classifications_status from this digitalisat.

        :param search_category_ids: A list of search_category ids.
        """
        if search_category_ids:
            classifications_status = [e for e in self.classifications_status
                                      if e.search_category_id in search_category_ids]
        else:
            classifications_status = self.classifications_status

        for cs in classifications_status:
            cs.delete()

    def has_classification_status(self, classification: Union[ClassificationStatusModel, str]):
        """
        True if this digitalisat has a status associate with a given SearchCategoryModel.

        :param classification: Either a  ClassificationStatusModel or a SearchCategoryModel id.
        :return:
        """
        if isinstance(classification, ClassificationStatusModel):
            return any([cs == classification for cs in self.classifications_status])
        else:
            return any([cs.search_category_id == classification for cs in self.classifications_status])

    def get_classification_status(self, search_category_id: str) -> Union[ClassificationStatusModel, None]:
        for cs in self.classifications_status:
            if cs.search_category_id == search_category_id:
                return cs
        return None

    def update_classification_status(self, search_category_id: str, status: ClassificationStatus):
        cs_model = self.get_classification_status(search_category_id)
        if cs_model:
            cs_model.status = status
            cs_model.save()

    def add_classification_status(self, search_category_id: str, status: ClassificationStatus,
                                  has_ownership: bool = False, has_location: bool = False,
                                  number_of_pages_classified=0):
        """
        Add a classification status for this digitalisat.

        Important!! After add you must call save() to send it to the database.

        :param search_category_id: The id of the SearchCategoryModel entity to be added.
        :param status: The status for this SearchCategoryModel
        :param has_ownership: True or False
        :param has_location: True or False
        :param number_of_pages_classified: the number of pages that were classified.

        :return:
        """
        classification_status_model = ClassificationStatusModel()
        classification_status_model.digitalisat_id = self.id
        classification_status_model.search_category_id = search_category_id
        classification_status_model.status = status
        classification_status_model.has_location = has_location
        classification_status_model.has_ownership = has_ownership
        classification_status_model.number_of_pages_classified = number_of_pages_classified
        # only add if it doesn't exists.
        if not self.has_classification_status(classification_status_model):
            self.classifications_status.append(classification_status_model)

    def set_unknown_classification(self, status=ClassificationStatus.OPEN):
        from flaskapp.models import SearchCategoryModel

        sc_model = SearchCategoryModel.get_unknown()
        if not sc_model:
            app_logger.info("Unknown or Default classification is not set in the database.")
            return

        # clear all classifications
        self.delete_classifications_status()

        self.add_classification_status(search_category_id=sc_model.id, status=status)
        self.save()

    def is_unclassified(self):
        """
        Return true if digitalisate is unclassified

        :return:
        """
        from flaskapp.models import SearchCategoryModel

        if len(self.classifications_status) == 0:
            return True

        elif len(self.classifications_status) == 1:
            sc_model = SearchCategoryModel.get_unknown()
            return self.classifications_status[0].search_category_id == sc_model.id
        else:
            return False

    def get_ocr_files(self, digitalisat_image_id: str) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        Gets the alto xml and json file path for the given image.

        :return: A tuple of strings with the file path for the alto and the json data if exists,
            otherwise it returns a tuple of None.
        """
        ocr_dir = self.ocr_dir
        alto_path = os.path.join(ocr_dir, f"{digitalisat_image_id}.xml")
        json_path = os.path.join(ocr_dir, f"{digitalisat_image_id}.json")
        if os.path.isfile(alto_path) and os.path.isfile(alto_path):
            return alto_path, json_path
        else:
            return None, None

    def locked_search_category_ids(self):
        """
        Get a list of search category ids that are locked for this digitalisat.

        :return: A list of search_category_ids
        """
        return [m.search_category_id for m in self.classifications_lock]

    @classmethod
    def advance_search(cls, digitalisate_search: DigitalisatSearch) -> SearchResult['DigitalisatModel']:

        from flaskapp.models import DigitalisatImageModel, DigitalisatImageOcrModel, ScopeDataModel, \
            SearchCategoryModel, ImageClassificationModel

        digitalisate_search: DigitalisatSearch

        order_method = desc if digitalisate_search.OrderDesc else asc

        # query = cls._create_query(digitalisate_search).distinct()
        search_filters = cls._construct_filter(digitalisate_search)
        query = select(cls).filter(*search_filters).distinct()

        joined_scope_model = False
        should_filter_text_and_category = False
        if not digitalisate_search.metadata.is_empty():
            meta = digitalisate_search.metadata
            search_by = "wohnort: lower[], registry_signature: lower[], " \
                        "geburtsname: lower[], dat_findbuch: lower[]"
            search_value = [meta.wohnort, meta.registrySignature, meta.geburtsname, meta.laufzeit]
            search_value = [v.strip() for v in search_value]
            meta_search = SearchDefault(SearchBy=search_by, SearchValue=search_value)
            scope_filters = ScopeDataModel._construct_filter(meta_search)

            if meta.title:
                text_search = parse_to_ts_query_string(meta.title)
                tsquery_func = func.to_tsquery(ScopeDataModel.LANGUAGE, text_search)
                scope_filters.append(
                    ScopeDataModel.title_vector.op('@@')(tsquery_func)
                )

            if meta.associates:
                text_search = parse_to_ts_query_string(meta.associates)
                tsquery_func = func.to_tsquery(ScopeDataModel.LANGUAGE, text_search)
                scope_filters.append(
                    ScopeDataModel.associates_vector.op('@@')(tsquery_func)
                )

            if meta.startSignature > 0:
                # noinspection PyTypeChecker
                scope_filters.append(cls.signature_number >= meta.startSignature)
            if meta.endSignature > 0:
                # noinspection PyTypeChecker
                scope_filters.append(cls.signature_number <= meta.endSignature)

            if val := digitalisate_search.metadata.comments:
                scope_filters.append(DigitalisatCommentsModel.comment.ilike(f"%{val}%"))
                query = query.join(DigitalisatCommentsModel)

            query = query.join(ScopeDataModel).filter(*scope_filters)
            joined_scope_model = True

        order_by_scope_data = ScopeDataModel._get_column_from_name(digitalisate_search.OrderBy)
        if order_by_scope_data is not None:
            query = query.add_columns(order_by_scope_data)
            if not joined_scope_model:
                query = query.join(ScopeDataModel)

            query = query.order_by(order_method(order_by_scope_data), cls.id)

        if digitalisate_search.classificationStatusId:
            if digitalisate_search.classificationStatus:
                filters = [
                    ClassificationStatusModel.search_category_id.__eq__(digitalisate_search.classificationStatusId),
                    ClassificationStatusModel.status.__eq__(digitalisate_search.classificationStatus)]
            else:
                filters = [
                    ClassificationStatusModel.search_category_id.__eq__(digitalisate_search.classificationStatusId)]

            query = query.join(ClassificationStatusModel, isouter=True).filter(*filters)

        if digitalisate_search.textSearch:

            text_search = parse_to_ts_query_string(digitalisate_search.textSearch)
            tsquery_func = func.to_tsquery(DigitalisatImageOcrModel.LANGUAGE, text_search)
            vector_subquery = (
                select(
                    DigitalisatImageModel.digitalisat_id)
                .distinct()
                .join(DigitalisatImageOcrModel)
                .where(DigitalisatImageOcrModel.search_vector.op('@@')(tsquery_func))
            )

            should_filter_text_and_category = \
                digitalisate_search.classificationStatusId \
                and digitalisate_search.classificationStatusId != SearchCategoryModel.get_unknown().id

            if should_filter_text_and_category:
                vector_subquery = (
                    vector_subquery
                    .join(ImageClassificationModel)
                    .where(ImageClassificationModel.search_category_id == digitalisate_search.classificationStatusId)
                )

            vector_subquery = vector_subquery.subquery()
            query = query.join(vector_subquery, DigitalisatModel.id.__eq__(vector_subquery.c.digitalisat_id))

        # Order by signature. This method extracts signature number and cast it to INT
        if digitalisate_search.OrderBy and digitalisate_search.OrderBy.lower() == "signature":
            order_by = [order_method(cls.signature_number), cls.id]
            # reset order_by and create a new one
            query = query.order_by(None).order_by(*order_by).options(undefer(cls.signature_number))

        # Order by page count
        elif digitalisate_search.OrderBy and digitalisate_search.OrderBy.lower() == "pagecount":
            query = query.order_by(None)
            # joined_tables = [mapper.class_ for mapper in query._join_entities]  # not working for sqlalchemy > 1.4
            # TODO Changed on sqlalchemy > 1.4 query._join_entities doesn't exists.
            #  Find a better way here thatn using query.statement._legacy_setup_joins
            if str(query.froms).find(DigitalisatImageModel.__tablename__) == -1:
                query = query.join(DigitalisatImageModel, isouter=True)

            count_col = func.count(DigitalisatImageModel.id).label("pagecount")
            query = query.group_by(cls.id).add_columns(count_col).order_by(order_method("pagecount"))

        # Order by number of pages in classification
        elif digitalisate_search.OrderBy and digitalisate_search.OrderBy.lower() == "matches" and \
                digitalisate_search.classificationStatusId:
            query = query.order_by(None)
            query = query.add_columns(ClassificationStatusModel.number_of_pages_classified)
            query = query.order_by(order_method(ClassificationStatusModel.number_of_pages_classified))

        try:
            page = db.paginate(query, per_page=digitalisate_search.per_page, page=digitalisate_search.page)

        except SQLAlchemyError as e:
            # cast to integer can fail and produce an exception
            db.session.rollback()
            query = query.order_by(None).order_by(*[order_method(cls.signature), cls.id])
            page = db.paginate(query, per_page=digitalisate_search.per_page, page=digitalisate_search.page)

        except werkzeug.exceptions.NotFound:
            page = db.paginate(query, per_page=digitalisate_search.per_page, page=1)

        entities = page.items
        total = page.total
        if entities:
            # add attribute text_filter and/or category_id.
            # When converting to dict this will be used to fetch only images that match the
            # text search term.
            if digitalisate_search.textSearch:
                all([setattr(obj, "text_filter", digitalisate_search.textSearch) for obj in entities])
                if should_filter_text_and_category:
                    all([setattr(obj, "category_id", digitalisate_search.classificationStatusId) for obj in entities])
            return SearchResult(entities, total)

        return SearchResult([], 0)
