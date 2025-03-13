import os
from typing import List

from flask_login import current_user

from flaskapp.controllers import digitalisat
from flaskapp.http_util import response as response
from flaskapp.http_util.caching import cacheable, delete_cache
from flaskapp.http_util.decorators import secure, post, query, query_param
from flaskapp.http_util.exceptions import EntityNotFound, AppException
from flaskapp.models import (Role, DigitalisatModel, DigitalisatCommentsModel, DigitalisatImageModel, \
                             DigitalisatImageOcrModel, ImageClassificationModel, ClassificationStatusModel,
                             ClassificationStatus,
                             SearchCategoryModel, Right)
from flaskapp.models.classifying_job_model import ClassifyingJobModel
from flaskapp.models.enums import DigitalisatStatus
from flaskapp.search.digitalisat_search import DigitalisatSearch
from flaskapp.services import DigitalisatService, NerService
from flaskapp.services.ocr_service import OcrDataParse
from flaskapp.structures import Cast
from flaskapp.structures.structures import SearchResult, SearchDefault


@digitalisat.route("/search", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query(DigitalisatSearch)
# @cacheable(timeout=60 * 5)
def search_digitalisate(digitalisat_search: DigitalisatSearch):
    search_result: SearchResult = DigitalisatService.advance_search(digitalisat_search)
    return response.model_to_response(search_result)


@digitalisat.route("/export-search", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query(DigitalisatSearch)
def export_search(digitalisat_search: DigitalisatSearch):
    file = DigitalisatService.export_search(digitalisat_search)
    return response.file_to_response(file, max_age=60, as_attachment=True, download_name="export_test.xlsx",
                                     mimetype="application/xlsx", delete_after=True)


@digitalisat.route("/<string:digitalisat_id>", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
def get_digitalisat(digitalisat_id: str):
    digitalisat_model: DigitalisatModel = DigitalisatModel.find_by_id(digitalisat_id)
    if digitalisat_model is None:
        raise EntityNotFound("Das Digitalisat konnte nicht ermittelt werden!")

    return response.model_to_response(digitalisat_model)


@digitalisat.route("/simpleSearch", methods=["GET"])
@query(SearchDefault)
@secure(Right.DIGITALISATE_VIEW)
def default_search(search: SearchDefault):
    search_result: SearchResult = DigitalisatService.search(search)
    return response.model_to_response(search_result)


@digitalisat.route("/totalOpenDigitalisateInCategory/", defaults={"category_id": None}, methods=["GET"])
@digitalisat.route("/totalOpenDigitalisateInCategory/<string:category_id>", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
def total_open_digitalisate_in_category(category_id: str):
    # TODO Try to make it direct in a query.
    models: List[DigitalisatModel] = \
        DigitalisatModel.get_digitalisate_with_open_or_no_classification(category_id)
    total = len(models)
    # filters = [ClassificationStatusModel.status == ClassificationStatus.OPEN]
    # if category_id:
    #     filters.append(ClassificationStatusModel.search_category_id == category_id)
    # total = ClassificationStatusModel.total(count_column=ClassificationStatusModel.digitalisat_id, filters=filters)
    return response.string_to_response(f"{total}")


@digitalisat.route("", methods=["PUT"])
@secure(Right.DIGITALISATE_UPDATE)
@post(class_to_map=DigitalisatModel)
# @delete_cache(value=search_digitalisate, delete_all=True)
def update_digitalisat(digitalisat_model: DigitalisatModel):
    if digitalisat_model:
        return response.model_to_response(DigitalisatService.update(digitalisat_model))
    raise AppException("Fehler beim Aktualisieren.")


@digitalisat.route("/getComments/<string:digitalisat_id>", methods=["GET"])
@secure(Right.COMMENT)
@cacheable(timeout=60*60)
def get_comments(digitalisat_id: str):
    models = DigitalisatCommentsModel.get_comments_from_digitalisat(digitalisat_id)
    return response.model_to_response(models)


@digitalisat.route("/addComment", methods=["POST"])
@secure(Right.COMMENT)
@post(class_to_map=DigitalisatCommentsModel)
@delete_cache(value=get_comments, delete_all=True)
def add_comment(digitalisat_comments_model: DigitalisatCommentsModel):
    dcm = DigitalisatCommentsModel.create_post(comment=digitalisat_comments_model.comment,
                                               digitalisat_id=digitalisat_comments_model.digitalisat_id,
                                               reference=digitalisat_comments_model.reference,
                                               user_id=current_user.user_id,
                                               comment_link_id=digitalisat_comments_model.comment_link_id)
    if dcm.save():
        return response.model_to_response(dcm)
    else:
        return response.empty_response()


@digitalisat.route("/updateComment", methods=["POST"])
@secure(Right.COMMENT)
@post(class_to_map=DigitalisatCommentsModel)
@delete_cache(value=get_comments, delete_all=True)
def update_comment(dto: DigitalisatCommentsModel):
    return response.bool_to_response(DigitalisatCommentsModel.update_comment(dto.id, dto.comment))


@digitalisat.route("/deleteComment/<string:comment_id>", methods=["DELETE"])
@secure(Right.COMMENT)
@delete_cache(value=get_comments, delete_all=True)
def delete_comment(comment_id):
    model: DigitalisatCommentsModel = DigitalisatCommentsModel.find_by_id(comment_id)
    if model:
        return response.bool_to_response(model.delete())
    return response.bool_to_response(False)


@digitalisat.route("/digitalisatImages", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query_param("digitalisatId", "textSearch")
def get_digitalisat_images(digitalisat_id: str, text_search: str):
    if text_search:
        images = DigitalisatImageModel.find_images_with_digitalisat_and_text(digitalisat_id, text_search)
        return response.model_to_response(images)

    model: DigitalisatModel = DigitalisatModel.find_by_id(digitalisat_id)
    if model:
        images = list(model.digitalisat_images)
        images.sort(key=lambda i: i.image_order)
        return response.model_to_response(images)
    return response.empty_response()


@digitalisat.route("/digitalisatImagesCategory", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query_param("digitalisatId", "categoryId", "textSearch")
def get_digitalisat_images_category(digitalisat_id: str, category_id: str, text_search):
    images = DigitalisatImageModel.find_images_with_digitalisat_and_classification(digitalisat_id, category_id,
                                                                                   text_search)
    if images:
        return response.model_to_response(images)
    return response.empty_response()


@digitalisat.route("/image", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query_param("imageId")
def get_image_file(image_id: str):
    model: DigitalisatImageModel = DigitalisatImageModel.find_by_id(image_id)
    if model:
        image_path = model.image_path
        if os.path.isfile(image_path):
            return response.file_to_response(image_path)
    return response.empty_response()


@digitalisat.route("/ocrData", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query_param("imageId")
@cacheable(timeout=60*10)
def get_image_ocr_data(image_id: str):
    model: DigitalisatImageOcrModel = DigitalisatImageOcrModel.find_by_id(image_id)
    if model:
        alto_path, json_path = model.get_ocr_files()
        if os.path.isfile(alto_path):
            ocr_data = OcrDataParse.parse_alto_xml(alto_path)
            # ocr_data = OcrDataParse.parse_alto_json(json_path)

            return response.dict_to_response(ocr_data.to_dict())
        raise AppException("Image has no ocr data")

    return response.empty_response()


@digitalisat.route("/foundTerms", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
@query_param("imageId", "categoryId")
@cacheable(timeout=60*10)
def get_found_terms(image_id: str, category_id: str):
    found_terms = ImageClassificationModel.get_found_terms(digitalisat_image_id=image_id, category_id=category_id)
    return response.jsonify(found_terms)


@digitalisat.route("/removeAllFileFromClassification/<string:digitalisat_id>/<string:category_id>", methods=["DELETE"])
@secure(Right.IMAGE_UPDATE)
def remove_all_image_from_classification(digitalisat_id: str, category_id: str):
    r = DigitalisatService.remove_all_digitalisat_image_from_classification(
        digitalisat_id=digitalisat_id, category_id=category_id
    )

    return response.bool_to_response(r)


@digitalisat.route("/removeFileFromClassification/<string:image_id>/<string:category_id>", methods=["DELETE"])
@secure(Right.IMAGE_UPDATE)
# @delete_cache(value=search_digitalisate, delete_all=True)
def remove_image_from_classification(image_id: str, category_id: str):
    r = DigitalisatService.remove_digitalisat_image_from_classification(image_id=image_id, category_id=category_id)

    return response.bool_to_response(r)


@digitalisat.route("/addFileToClassification", methods=["POST"])
@secure(Right.IMAGE_UPDATE)
@post("image_id", "category_id")
# @delete_cache(value=search_digitalisate, delete_all=True)
def add_file_to_classification(image_id: str, category_id: str):
    r = DigitalisatService.add_digitalisat_image_to_classification(image_id=image_id, category_id=category_id)

    return response.bool_to_response(r)


@digitalisat.route("/changeClassificationStatus", methods=["POST"])
@secure(Right.IMAGE_UPDATE)
@post("digitalisat_id", "category_id", "status")
# @delete_cache(value=search_digitalisate, delete_all=True)
def change_classification_status(digitalisat_id: str, category_id: str, status: str):
    cs_model: ClassificationStatusModel = \
        ClassificationStatusModel.find_by(digitalisat_id=digitalisat_id, search_category_id=category_id, get_first=True)

    r = False
    if cs_model:
        cs_model.status = ClassificationStatus[status]
        r = cs_model.save()

    return response.bool_to_response(r)


@digitalisat.route("/unlockDigitalisatClassification", methods=["POST"])
@secure(Right.DIGITALISATE_UPDATE)
@post("digitalisat_id", "category_id")
def unlock_digitalisat_classification(digitalisat_id: str, category_id: str):
    if DigitalisatService.unlock_digitalisate_in_classification(digitalisat_id=digitalisat_id, category_id=category_id):
        return response.model_to_response(DigitalisatModel.find_by_id(digitalisat_id))
    return response.empty_response()


@digitalisat.route("/changeClassificationOwnership", methods=["POST"])
@secure(Right.DIGITALISATE_UPDATE)
@post("digitalisat_id", "category_id", "has_ownership")
# @delete_cache(value=search_digitalisate, delete_all=True)
def change_classification_ownership(digitalisat_id: str, category_id: str, has_ownership: bool):
    cs_model: ClassificationStatusModel = \
        ClassificationStatusModel.find_by(digitalisat_id=digitalisat_id, search_category_id=category_id, get_first=True)

    r = False
    if cs_model:
        cs_model.has_ownership = has_ownership
        r = cs_model.save()

    return response.bool_to_response(r)


@digitalisat.route("/changeClassificationLocation", methods=["POST"])
@secure(Right.DIGITALISATE_UPDATE)
@post("digitalisat_id", "category_id", "has_location")
# @delete_cache(value=search_digitalisate, delete_all=True)
def change_classification_location(digitalisat_id: str, category_id: str, has_location: bool):
    cs_model: ClassificationStatusModel = \
        ClassificationStatusModel.find_by(digitalisat_id=digitalisat_id, search_category_id=category_id, get_first=True)

    r = False
    if cs_model:
        cs_model.has_location = has_location
        r = cs_model.save()

    return response.bool_to_response(r)


@digitalisat.route("/reclassifyDigitalisat", methods=["POST"])
@secure(Right.RECLASSIFY)
@post("digitalisat_id", "category_id")
# @delete_cache(value=search_digitalisate, delete_all=True)
def reclassify_digitalisat(digitalisat_id: str, category_id: str):
    model: DigitalisatModel = DigitalisatModel.find_by_id(digitalisat_id)
    search_category = SearchCategoryModel.find_by_id(category_id)
    search_category = [search_category] if search_category else None
    if model:
        DigitalisatService.classify_digitalisat(model, status_during_classification=DigitalisatStatus.RECLASSIFYING,
                                                search_categories=search_category)
        return response.model_to_response(model)
    return response.empty_response()


@digitalisat.route("/addToReclassifyJob", methods=["POST"])
@secure(Right.RECLASSIFY)
@post("category_id")
# @delete_cache(value=search_digitalisate, delete_all=True)
def add_to_reclassify_job(category_id: str):
    job_id = 'reclassify_digitalisate'
    ClassifyingJobModel.add_job(job_id=job_id, category_id=category_id, total_files=0)
    return response.string_to_response(job_id)


@digitalisat.route("/isClassificationRunning", methods=["GET"])
@secure(Right.RECLASSIFY)
def is_classification_running():
    job_id = 'reclassify_digitalisate'
    cj: ClassifyingJobModel = ClassifyingJobModel.find_by_id(job_id)
    if cj:
        return response.bool_to_response(cj.is_in_progress())
    return response.bool_to_response(False)


@digitalisat.route("/info", methods=["GET"])
@secure(Role.ADMIN)
def get_info():
    result = DigitalisatService.get_info()
    return response.model_to_response(result)


@digitalisat.route("/imageNERs", methods=["GET"])
@query_param("image_id", "clean_text")
@secure()
def get_image_ners(image_id: str, clean_text=True):
    clean_text = Cast(clean_text, bool)
    found_entities = NerService.construct_image_ner(image_id, clean_text=clean_text)
    return response.model_to_response(found_entities)
