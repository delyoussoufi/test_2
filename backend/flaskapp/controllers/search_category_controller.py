from typing import List

from flaskapp import app_logger
from flaskapp.controllers import search_category
from flaskapp.http_util import response as response
from flaskapp.http_util.decorators import secure, query, post
from flaskapp.http_util.exceptions import AppException, EntityNotFound
from flaskapp.models import SearchCategoryModel, Right
from flaskapp.services import SearchCategoryService
from flaskapp.structures.structures import SearchResult, Search


@search_category.route("/search", methods=["GET"])
@secure(Right.CATEGORY_VIEW, Right.DIGITALISATE_VIEW)
@query(Search)
def search_categories(category_search: Search):
    search_result: SearchResult = SearchCategoryModel.search(category_search)
    return response.model_to_response(search_result)


@search_category.route("/<string:search_category_id>", methods=["GET"])
@secure(Right.CATEGORY_VIEW, Right.DIGITALISATE_VIEW)
def get_search_category(search_category_id: str):
    search_category_model: SearchCategoryModel = SearchCategoryModel.find_by_id(search_category_id)
    if search_category_model is None:
        raise EntityNotFound("Die Suchkategorie konnte nicht ermittelt werden!")

    return response.model_to_response(search_category_model)


@search_category.route("/all", methods=["GET"])
@secure(Right.DIGITALISATE_VIEW)
def get_all_search_categories():
    search_category_model: List[SearchCategoryModel] = SearchCategoryModel.get_all(order_by='order')
    return response.model_to_response(search_category_model)


@search_category.route("", methods=["POST"])
@secure(Right.CATEGORY_EDIT)
@post(class_to_map=SearchCategoryModel)
def create_category(category_model: SearchCategoryModel):
    return response.model_to_response(SearchCategoryService.create(category_model))


@search_category.route("/reorder", methods=["POST"])
@secure(Right.CATEGORY_EDIT)
@post(class_to_map=SearchCategoryModel)
def reorder_categories(categories_model: List[SearchCategoryModel]):
    return response.bool_to_response(SearchCategoryService.reorder(categories_model))


@search_category.route("<string:category_id>", methods=["DELETE"])
@secure(Right.CATEGORY_EDIT)
def delete_category(category_id: str):
    category_model: SearchCategoryModel = SearchCategoryModel.find_by_id(category_id)
    if category_model is None:
        raise EntityNotFound(f"Die Suchkategorie {category_id} konnte nicht gefunden werden.")
    deleted = category_model.delete()
    if deleted:
        app_logger.info(f"Die Suchkategorie {category_id} wurde gelöscht.")
    else:
        app_logger.warning(f"Die Suchkategorie {category_id} konnte nicht gelöscht werden.")
    return response.bool_to_response(deleted)


@search_category.route("", methods=["PUT"])
@secure(Right.CATEGORY_EDIT)
@post(class_to_map=SearchCategoryModel)
def update_search_category(search_category_model: SearchCategoryModel):
    if search_category_model:
        return response.model_to_response(SearchCategoryService.update(search_category_model))
    raise AppException("Fehler beim Aktualisieren.")


@search_category.route("exportSearchCategoriesExcel", methods=["POST"])
@secure(Right.CATEGORY_EDIT)
def export_search_categories_excel():
    excel_file_path = SearchCategoryService.export_excel()
    return response.file_to_response(excel_file_path, delete_after=True)


@search_category.route("exportSearchCategoriesExcelSearch", methods=["POST"])
@secure(Right.CATEGORY_EDIT)
@query(Search)
def export_search_categories_excel_search(category_search: Search):
    search_result: SearchResult = SearchCategoryModel.search(category_search)
    excel_file_path = SearchCategoryService.export_excel_for_search(search_result)
    return response.file_to_response(excel_file_path, delete_after=True)


@search_category.route("/export-classification-results/<string:category_id>", methods=["GET"])
@secure(Right.CATEGORY_VIEW)
def export_classification_results(category_id: str):
    file = SearchCategoryService.export_category_results(category_id)
    return response.file_to_response(file, max_age=60, as_attachment=True, download_name="export_test.xlsx",
                                     mimetype="application/xlsx", delete_after=True)
