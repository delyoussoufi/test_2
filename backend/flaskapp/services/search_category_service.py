import io
import tempfile
from typing import List

from flaskapp import app_utils
from flaskapp.excel import ExcelWriter
from flaskapp.http_util.exceptions import AppException, EntityNotFound
from flaskapp.models import SearchCategoryModel, SearchTermModel, BlacklistTermModel, NonRelevantTermModel, \
    ClassificationStatusModel, DigitalisatModel, DigitalisatImageModel, ImageClassificationModel
from flaskapp.search import SearchCategorySearch
from flaskapp.services.digitalisat_search_category_results_exporter_service import \
    DigitalisatSearchCategoryResultsExporterService
from flaskapp.structures.structures import SearchResult


class SearchCategoryService:

    @staticmethod
    def search(search_category_search: SearchCategorySearch) -> SearchResult:
        return SearchCategoryModel.search(search_category_search)

    @classmethod
    def create(cls, category_model: SearchCategoryModel) -> SearchCategoryModel:
        SearchCategoryService.check_category_dto(category_model)
        if SearchCategoryModel.find_by(name=category_model.name):
            raise AppException("This name already exists.")
        category_model.id = app_utils.generate_id(16)
        for search_term in category_model.search_terms:
            search_term.id = app_utils.generate_id(16)
        if not category_model.save():
            raise AppException("Couldn't create this category.")
        return category_model

    @staticmethod
    def update(category_model: SearchCategoryModel) -> SearchCategoryModel:
        SearchCategoryService.check_category_dto(category_model)
        existing_model: SearchCategoryModel = SearchCategoryModel.find_by_id(category_model.id)
        existing_model.delete_search_terms()
        existing_model.delete_blacklist_terms()
        existing_model.delete_non_relevant_terms()
        existing_model << category_model
        for search_term in category_model.search_terms:
            existing_model.search_terms.append(SearchTermModel(
                id=app_utils.generate_id(16), category_id=existing_model.id, search_value=search_term.search_value))
        for black_list in category_model.blacklist_terms:
            existing_model.blacklist_terms.append(BlacklistTermModel(
                id=app_utils.generate_id(16), category_id=existing_model.id, value=black_list.value))
        for non_relevant_term in category_model.non_relevant_terms:
            existing_model.non_relevant_terms.append(NonRelevantTermModel(
                id=app_utils.generate_id(16), category_id=existing_model.id, value=non_relevant_term.value))

        existing_model.save()
        return existing_model

    @classmethod
    def reorder(cls, categories_model: List[SearchCategoryModel]):
        models_to_save = []
        for sc in categories_model:
            exiting_model: SearchCategoryModel = SearchCategoryModel.find_by_id(sc.id)
            if exiting_model and exiting_model.order != sc.order:
                exiting_model.order = sc.order
                models_to_save.append(exiting_model)

        return SearchCategoryModel.bulk_save(models_to_save)

    @staticmethod
    def export_excel() -> str:
        sc_models = SearchCategoryModel.get_all(order_by=SearchCategoryModel.name)
        search_result = SearchResult(sc_models, len(sc_models))
        return SearchCategoryService.__create_workbook(search_result)

    @staticmethod
    def export_excel_for_search(search_result) -> str:
        return SearchCategoryService.__create_workbook(search_result)

    @staticmethod
    def __create_workbook(search_result) -> str:
        temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", mode='w+t', delete=False)
        temp_file_path = temp_file.name
        temp_file.close()
        headers = ["Name", "Beschreibung", "Suchbegriffe"]
        excel_data = []
        for category in search_result.resultList:
            category_dict = category.to_dict()
            search_terms = [search_term.search_value for search_term in category.search_terms]
            row = [category_dict.get("name", ""), category_dict.get("description", None), ', '.join(search_terms)]

            excel_data.append(row)
        ExcelWriter.write_excel(temp_file_path, "Suchkategorien", headers, excel_data)
        return temp_file_path

    @classmethod
    def check_category_dto(cls, category_model: SearchCategoryModel):
        if not category_model.name:
            raise AppException("Kein Name erfasst!")

    @staticmethod
    def export_category_results(category_id: str) -> io.BytesIO:
        search_category_model = SearchCategoryModel.find_by_id(category_id)
        if not search_category_model:
            raise EntityNotFound(f"Couldn't find category {category_id}.")

        out_path = io.BytesIO()
        try:
            export_service = DigitalisatSearchCategoryResultsExporterService(excel_file_path=out_path)
            export_service.export(search_category_model)
        finally:
            out_path.seek(0)
            out_path.flush()
        return out_path
