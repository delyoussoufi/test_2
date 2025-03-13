from io import BytesIO
from typing import Union, Optional

from xlsxwriter.worksheet import Worksheet

from flaskapp import active_config
from flaskapp.excel import ExcelBaseWriter
from flaskapp.models import DigitalisatModel, DigitalisatImageModel, ScopeDataModel, SearchCategoryModel, \
    SearchTermModel, ClassificationStatusModel, ImageClassificationModel
from flaskapp.structures.structures import SearchResult
from flaskapp.utils import DateUtils


class DigitalisatSearchCategoryResultsExporterService(ExcelBaseWriter):

    def __init__(self, excel_file_path: Union[BytesIO, str]):
        super().__init__(excel_file_path)
        self.headers = [
            "ScopeId",
            "Aktensignatur",
            "Registratursignatur",
            "Name",
            "View link",
        ]
        self.view_url: str = active_config.SCOPE_DETAIL_VIEW_URL

    def _filter_images(self, digitalisat: DigitalisatModel) -> int:
        text_filter = getattr(digitalisat, "text_filter", None)
        if text_filter:
            self._text_search = text_filter
            return digitalisat.number_of_images(text_filter, getattr(digitalisat, "category_id", None))

        return digitalisat.expected_images

    def get_match_pages(self,  digitalisat: DigitalisatModel):
        if self._text_search:
            return ", ".join(
                [
                    f"{image.image_order}" for image in
                    DigitalisatImageModel.find_images_with_digitalisat_and_text(digitalisat.id, self._text_search)
                ]
            )

        return ""

    def _write_filter_info(self, worksheet: Worksheet, at=(0, 0), category_name: str = ""):
        row, col = at
        worksheet.write(row, col, f"Suchkategorie = {category_name}", self.header_format)

    def _get_page_matches(self, digitalisat: DigitalisatModel, search_category_model: SearchCategoryModel):
        images = DigitalisatImageModel.find_images_with_digitalisat_and_classification(
            digitalisat_id=digitalisat.id, category_id=search_category_model.id
        )
        _matches = {f"{term.search_value}": [] for term in search_category_model.search_terms}
        _matches["None"] = []

        [
            _matches[term["value"]].append(f"{image.image_order}")
            for image in images
            for term in
            ImageClassificationModel.get_found_terms(
                digitalisat_image_id=image.id,
                category_id=search_category_model.id,
            )
        ]

        return _matches

    def _write_data(self, worksheet: Worksheet, digitalisat: DigitalisatModel,
                    search_category_model: SearchCategoryModel):
        scope_data: ScopeDataModel = digitalisat.scope_data

        data = [
            digitalisat.scope_id,
            digitalisat.signature,
            scope_data.registry_signature,
            scope_data.title,
            f"{self.view_url}{digitalisat.scope_id}"
        ]

        data.extend(
            [
                ", ".join(pages_order) for pages_order in
                self._get_page_matches(digitalisat, search_category_model).values()
            ]
        )

        for i, value in enumerate(data):
            worksheet.write(self._current_row, i, value, self.data_format)
        self._current_row += 1

    def export(self, search_category_model: SearchCategoryModel, worksheet_name: str = None):
        # extend headers based on search terms
        self.headers.extend(
            (
                f"'{term.search_value}' gefunden auf Seite"
                for term in search_category_model.search_terms
            )
        )

        self.headers.append("Manuell hinzugefügte Seiten")

        # gets all digitalisate that belong to this search category
        digitalisate = (
            entity.digitalisat for entity in
            ClassificationStatusModel.find_by(search_category_id=search_category_model.id, get_first=False)
        )

        try:
            # Add a bold format to use to highlight cells.
            worksheet = self.workbook.add_worksheet(worksheet_name)
            self._write_headers(worksheet, row_offset=2)

            for digitalisat in digitalisate:
                self._write_data(worksheet, digitalisat, search_category_model)

            self._write_filter_info(worksheet, category_name=search_category_model.name)
            worksheet.autofit()
        finally:
            self.workbook.close()
            self._workbook = None

