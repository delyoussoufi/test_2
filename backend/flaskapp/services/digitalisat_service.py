import io
import os
from collections import Counter
from pathlib import Path
from typing import List

from sqlalchemy import func

from flaskapp import app_utils, app_logger
from flaskapp.classification.data_structure import SearchTerm
from flaskapp.classification.finder_gram_levenshtein_model import FinderGramLevenshteinModelMultiple
from flaskapp.http_util.exceptions import AppException
from flaskapp.http_util.lock_utils import LockById
from flaskapp.models import DigitalisatModel, DigitalisatImageModel, SearchCategoryModel, \
    ImageClassificationModel, ClassificationStatus, ClassificationStatusModel, DigitalisatClassificationLockModel
from flaskapp.models.classifying_job_model import ClassifyingJobModel
from flaskapp.models.enums import DigitalisatStatus
from flaskapp.search.digitalisat_search import DigitalisatSearch
from flaskapp.services.digitalisat_search_exporter_service import DigitalisatSearchExporterService
from flaskapp.services.ocr_service import OcrDataParse
from flaskapp.services.scope_service import DigitalisatScopeInfo
from flaskapp.services_async.reclassify_async_service import ReclassifyDigitalisateService
from flaskapp.structures import OcrData
from flaskapp.structures.structures import SearchResult, SearchDefault, DigitalisateInfo
from flaskapp.utils import FileUtils


class DigitalisatService:

    @staticmethod
    def search(search: SearchDefault) -> SearchResult[DigitalisatModel]:
        return DigitalisatModel.search(search)

    @staticmethod
    def advance_search(digitalisat_search: DigitalisatSearch) -> SearchResult[DigitalisatModel]:
        return DigitalisatModel.advance_search(digitalisat_search)

    @staticmethod
    def export_search(digitalisat_search: DigitalisatSearch):
        digitalisat_search.Page = 1
        digitalisat_search.PerPage = 10000
        result: SearchResult = DigitalisatModel.advance_search(digitalisat_search)

        out_path = io.BytesIO()
        try:
            export_service = DigitalisatSearchExporterService(excel_file_path=out_path)
            export_service.export(result)
        finally:
            out_path.seek(0)
            out_path.flush()
        return out_path

    @staticmethod
    def create(digitalisat_model: DigitalisatModel) -> DigitalisatModel:
        DigitalisatService.check_digitalisat_dto(digitalisat_model)
        digitalisat_model.id = app_utils.generate_id(16)
        digitalisat_model.save()
        return digitalisat_model

    @staticmethod
    def update(digitalisat_model: DigitalisatModel) -> DigitalisatModel:
        DigitalisatService.check_digitalisat_dto(digitalisat_model)
        existing_model = DigitalisatModel.find_by_id(digitalisat_model.id)
        existing_model << digitalisat_model
        existing_model.save()
        return existing_model

    @staticmethod
    def check_digitalisat_dto(digitalisat_model: DigitalisatModel):
        if not digitalisat_model.signature:
            raise AppException("Keine Signatur erfasst!")

    @classmethod
    def classify_digitalisat_image(cls, digitalisat_image_model: DigitalisatImageModel,
                                   search_categories: List[SearchCategoryModel]) -> List[SearchCategoryModel]:

        alto_path, _ = digitalisat_image_model.get_ocr_files()
        if not alto_path:
            app_logger.error(f"Image {digitalisat_image_model.id} has no OCR alto.")
            return []

        found_categories = []
        ocr_data: OcrData = OcrDataParse.parse_alto_xml(alto_path)
        # try to classify this image for each given category.
        for sc in search_categories:
            # delete classifications associate to this image.
            digitalisat_image_model.delete_image_classification(search_category_id=sc.id)
            found_terms = FinderGramLevenshteinModelMultiple.find_words(
                ocr_data=ocr_data.to_dict(),
                search_terms=sc.get_all_search_terms(),
                no_relevant_terms=sc.get_all_non_relevant_terms(),
                black_list_terms=sc.get_all_blacklist_terms()
            )
            if found_terms:
                # append this category if terms were found.
                found_categories.append(sc)
                # add classification to this image if terms were found.
                digitalisat_image_model.add_classification(category_id=sc.id, found_terms=found_terms)

        # save image if search terms were found.
        if found_categories:
            digitalisat_image_model.save()

        return found_categories

    @classmethod
    def classify_digitalisat(cls, digitalisat_model: DigitalisatModel,
                             search_categories: List[SearchCategoryModel] = None,
                             status_during_classification=DigitalisatStatus.CLASSIFYING):

        digitalisat_model.status = status_during_classification
        try:
            if search_categories is None:
                search_categories: List[SearchCategoryModel] = SearchCategoryModel.get_categories_without_default()
                # remove all classifications from this digitalisat.
                digitalisat_model.delete_classifications_status()
            else:
                # remove the given classifications from this digitalisat.
                search_category_ids = [e.id for e in search_categories]
                # append unknown classification so it can also be removed.
                sc_unknown_id = SearchCategoryModel.get_unknown().id
                if sc_unknown_id not in search_category_ids:
                    search_category_ids.append(sc_unknown_id)
                digitalisat_model.delete_classifications_status(search_category_ids=search_category_ids)

            # remove search_categories that are locked for this digitalisat
            locked_search_category_ids = digitalisat_model.locked_search_category_ids()
            search_categories = [sc for sc in search_categories if sc.id not in locked_search_category_ids]

            if digitalisat_model.save() and len(search_categories) > 0:
                # Initialize the counter for found categories
                digitalisat_found_categories = Counter()
                digitalisat_found_categories.update(
                    fc.id
                    for digitalisat_image in digitalisat_model.digitalisat_images
                    for fc in cls.classify_digitalisat_image(digitalisat_image, search_categories)
                )

                if digitalisat_found_categories:
                    [
                        digitalisat_model.add_classification_status(
                            search_category_id=sc_id,
                            status=ClassificationStatus.OPEN,
                            number_of_pages_classified=number_of_pages_classified
                        )
                        for sc_id, number_of_pages_classified in digitalisat_found_categories.items()
                    ]
                else:
                    if not digitalisat_model.classifications_status:
                        digitalisat_model.set_unknown_classification()

        finally:
            digitalisat_model.status = DigitalisatStatus.FINISHED
            digitalisat_model.save()

    @classmethod
    def run_classify(cls):
        models = DigitalisatModel.get_classifying_status()
        models.extend(DigitalisatModel.get_ocr_finished_status())
        for digitalisat_model in models:
            cls.classify_digitalisat(digitalisat_model)

    @classmethod
    def rerun_classification(cls, cj: ClassifyingJobModel,  category_id=""):

        ids_: List[str] = [
            m.id for m in
            DigitalisatModel.get_digitalisate_with_open_or_no_classification(category_id)
        ]

        search_category = SearchCategoryModel.find_by_id(category_id)
        search_category = [search_category] if search_category else None
        cj.total_files = len(ids_)
        cj.save()
        with (LockById(lock_id="reclassify") and
              ReclassifyDigitalisateService(
                  digitalisate_ids=ids_,
                  search_category=search_category
              ) as async_reclassify_service):

            async_reclassify_service.update = cj.update_process
            async_reclassify_service.register_classification_job(cls.classify_digitalisat)
            async_reclassify_service.run_tasks()

            # for n, model in enumerate(models):
            #     if search_category is None:
            #         if not model.is_unclassified():
            #             # If no category is defined gets only the ones with open status excluding unclassified
            #             search_category = SearchCategoryModel.get_categories_without_default()
            #             black_list = {cs.search_category for cs in model.classifications_status
            #                           if cs.status != ClassificationStatus.OPEN}
            #             search_category = list(set(search_category).difference(black_list))
            #
            #     cls.classify_digitalisat(
            #         model,
            #         status_during_classification=DigitalisatStatus.RECLASSIFYING,
            #         search_categories=search_category
            #     )
            #
            #     cj.update_process(n + 1)

    @classmethod
    def validate_digitalisate_classification(cls, digitalisat_id: str):
        """
        Validate the digitalisate classification. If it is unclassified then it reinforces that it will be set as
        unknown classification, otherwise it makes sure unknown classification is removed.

        :param digitalisat_id:
        :return:
        """
        digitalisat: DigitalisatModel = DigitalisatModel.find_by_id(digitalisat_id)
        if not digitalisat:
            return

        if digitalisat.is_unclassified():
            # if digitalisat is unclassified or has no classification, this forces an unknown_classification
            digitalisat.set_unknown_classification()
        else:
            # remove unknown_classification if exist
            unknown_sc = SearchCategoryModel.get_unknown()
            for cs in digitalisat.classifications_status:
                if cs.search_category_id == unknown_sc.id:
                    cs.delete()

    @classmethod
    def update_classification_status(cls, digitalisat_id: str, category_id: str) -> bool:
        """
        Update the classification status for this digitalisat. If no image is found it will
        remove and lock this digitalisat from this classification.
        :param digitalisat_id:
        :param category_id:
        :return: True if successfully, false otherwise.
        """

        # get the classification status object for this digitalisat.
        cs_model: ClassificationStatusModel = \
            ClassificationStatusModel.find_by(digitalisat_id=digitalisat_id, search_category_id=category_id)

        if not cs_model:
            # nothing to do.
            return True

        # counts the number of images classified in this category for this digitalisat.
        classify_pages = \
            ClassificationStatusModel.number_of_images_in_digitalisat_and_classification(digitalisat_id,
                                                                                         category_id)
        # set the new number of images classified.
        cs_model.number_of_pages_classified = classify_pages
        if cs_model.number_of_pages_classified == 0:
            deleted = cs_model.delete()
            cls.lock_digitalisate_in_classification(digitalisat_id=digitalisat_id, category_id=category_id)
            # validate digitalisate if no classification is found it will set to unclassified.
            cls.validate_digitalisate_classification(digitalisat_id)
            return deleted
        else:
            return cs_model.save()

    @classmethod
    def remove_all_digitalisat_image_from_classification(cls, digitalisat_id: str, category_id: str) -> bool:
        deleted = ImageClassificationModel.delete_images_from_classification(
            digitalisat_id=digitalisat_id,
            search_category_id=category_id
        )
        if deleted:
            return cls.update_classification_status(digitalisat_id=digitalisat_id, category_id=category_id)

        return deleted

    @classmethod
    def remove_digitalisat_image_from_classification(cls, image_id: str, category_id: str) -> bool:
        ic_model: ImageClassificationModel = ImageClassificationModel.find_by(digitalisat_image_id=image_id,
                                                                              search_category_id=category_id,
                                                                              get_first=True)
        if ic_model:
            # get digitalisat via backref
            digitalisat_id = ic_model.digitalisat_image.digitalisat_id  # backref
            # delete image_classification object
            if digitalisat_id and ic_model.delete():
                # update status of classification on digitalisat level.
                return cls.update_classification_status(digitalisat_id=digitalisat_id, category_id=category_id)

        return False

    @classmethod
    def add_digitalisat_image_to_classification(cls, image_id: str, category_id: str) -> bool:
        # can't add to unknown
        if category_id == SearchCategoryModel.get_unknown().id:
            return False

        digitalisat_image_model: DigitalisatImageModel = DigitalisatImageModel.find_by_id(image_id)

        digitalisat_id = digitalisat_image_model.digitalisat_id
        if DigitalisatClassificationLockModel.is_locked(digitalisat_id, category_id):
            raise AppException("The current digitalisate is locked for this category. "
                               "Please, unlock it to add images.")

        if digitalisat_image_model:
            digitalisat_image_model.add_classification(category_id=category_id,
                                                       found_terms=[SearchTerm(value="None", found_terms=[])])
            if digitalisat_image_model.save():
                # get the classification status object for this digitalisat.
                cs_model: ClassificationStatusModel = \
                    ClassificationStatusModel.find_by(digitalisat_id=digitalisat_id, search_category_id=category_id)
                classify_pages = \
                    ClassificationStatusModel.number_of_images_in_digitalisat_and_classification(digitalisat_id,
                                                                                                 category_id)
                if cs_model:
                    # counts the number of images classified in this category for this digitalisat.
                    # set the new number of images classified.
                    cs_model.number_of_pages_classified = classify_pages
                    return cs_model.save()
                elif not cs_model and classify_pages > 0:
                    # if ClassificationStatusModel doesn't exist but images were added to its classification than
                    # add this classification also to digitalisat.
                    digitalisat_model = digitalisat_image_model.digitalisat  # backref
                    digitalisat_model.add_classification_status(search_category_id=category_id,
                                                                status=ClassificationStatus.OPEN,
                                                                number_of_pages_classified=classify_pages)
                    saved = digitalisat_model.save()
                    cls.validate_digitalisate_classification(digitalisat_id)
                    return saved

        return False

    @staticmethod
    def synchronize_scope_data():
        """
        Synchronize scope data for all digitalisat.

        :return:
        """

        app_logger.info('Scope synchronization started.')

        digitalisat_iter = (d for d in DigitalisatModel.get_all())
        DigitalisatScopeInfo.clear_scope_elements_mapper()  # clear cached scope elements.

        for model in digitalisat_iter:
            model: DigitalisatModel
            model.synchronize_scope_data()

        app_logger.info('Scope synchronization ended.')

    @classmethod
    def lock_digitalisate_in_classification(cls, digitalisat_id: str, category_id: str):
        """
        Lock the given digitalisate for the given classification.

        :param digitalisat_id:
        :param category_id:
        :return:
        """

        lock_model = DigitalisatClassificationLockModel.find_by_id(digitalisat_id, category_id)

        if not lock_model:
            lock_model = DigitalisatClassificationLockModel(digitalisat_id=digitalisat_id,
                                                            search_category_id=category_id)
            lock_model.save()

    @classmethod
    def unlock_digitalisate_in_classification(cls, digitalisat_id: str, category_id: str):
        """
        Unlock the given digitalisate for the given classification.

        :param digitalisat_id:
        :param category_id:
        :return:
        """

        lock_model = DigitalisatClassificationLockModel.find_by_id(digitalisat_id, category_id)

        if lock_model:
            lock_model: DigitalisatClassificationLockModel
            return lock_model.delete()
        return True

    @classmethod
    def create_sub_folder(cls, target_dir: str, limit: int):
        """
        Creates or gets the sub-folder where the digitalisat should be storage.

        :param target_dir: The root directory to create sub-folders.
        :param limit: The maximum number of digitalisat in a sub-folder. If limit is reach it creates the next.
        :return: The sub-folder to store the digitalisat.
        """

        # Clean list of files that is not numeric.
        files = [folder for folder in FileUtils.get_subfolders(target_dir)
                 if (FileUtils.get_folder_name_from_path(folder).isnumeric())]

        if len(files) == 0:
            sub_folder = os.path.join(target_dir, "1")
            Path(sub_folder).mkdir(parents=True)
            if not os.path.exists(sub_folder):
                return None
        else:
            files.sort(key=lambda f: int(FileUtils.get_folder_name_from_path(f)))
            last_folder_name = os.path.basename(files[- 1])
            sub_folder = os.path.join(target_dir, last_folder_name)
            if os.path.exists(sub_folder):
                num_of_digitalisat = len(FileUtils.get_subfolders(sub_folder))
                # Subdirectory is full. Create a new one.
                if num_of_digitalisat >= limit:
                    new_folder_name = str(int(last_folder_name) + 1)
                    sub_folder = os.path.join(target_dir, new_folder_name)
                    Path(sub_folder).mkdir(parents=True)
                    if not os.path.exists(sub_folder):
                        return None
            else:
                print("At this point this folder should exist.")
                return None

        return sub_folder

    @classmethod
    def get_info(cls) -> List[DigitalisateInfo]:
        """
        Gets information about digitalisate. How many digitalisate in each status exits.

        :return:
        """

        query = DigitalisatModel.query.session.query(
            DigitalisatModel.status,
            func.count(DigitalisatModel.id),
        ).group_by(
            DigitalisatModel.status,
        ).order_by(DigitalisatModel.status)

        return [DigitalisateInfo(status=r[0].value, total=r[1]) for r in query]
