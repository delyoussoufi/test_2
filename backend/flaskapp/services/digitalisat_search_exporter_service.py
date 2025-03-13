from io import BytesIO
from typing import Union, Optional

from xlsxwriter.worksheet import Worksheet

from flaskapp import active_config
from flaskapp.excel import ExcelBaseWriter
from flaskapp.models import DigitalisatModel, DigitalisatImageModel, ScopeDataModel
from flaskapp.structures.structures import SearchResult
from flaskapp.utils import DateUtils


class DigitalisatSearchExporterService(ExcelBaseWriter):

    def __init__(self, excel_file_path: Union[BytesIO, str]):
        super().__init__(excel_file_path)
        self.headers = [
            "ScopeId",
            "Aktensignatur",
            "Registratursignatur",
            "Name",
            "Geburtsname",
            "Laufzeit",
            "Geburtsort",
            "Geburtsdatum",
            "Wohnort",
            "in Akte genannt",
            "Total Images",
            "Filtered Images",
            "Found in pages",
            "View link"
        ]
        self._text_search: Optional[str] = None

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

    def _write_filter_info(self, worksheet: Worksheet, at=(0, 0)):
        row, col = at
        text_search = self._text_search if self._text_search else ''
        worksheet.write(row, col, f"Text Filter = {text_search}", self.header_format)

    def _write_data(self, worksheet: Worksheet, digitalisat: DigitalisatModel):
        scope_data: ScopeDataModel = digitalisat.scope_data
        data = [
            digitalisat.scope_id,
            digitalisat.signature,
            scope_data.registry_signature,
            scope_data.title,
            scope_data.geburtsname,
            scope_data.dat_findbuch,
            scope_data.geburtsort,
            DateUtils.convert_date_to_german_string(scope_data.geburtsdatum),
            scope_data.wohnort,
            scope_data.associates,
            digitalisat.number_of_images(),
            self._filter_images(digitalisat),
            self.get_match_pages(digitalisat),
            f"{self.view_url}{digitalisat.scope_id}"
        ]
        for i, value in enumerate(data):
            worksheet.write(self._current_row, i,value, self.data_format)
        self._current_row += 1

    def export(self, search_result: SearchResult, worksheet_name: str = None):
        try:
            # Add a bold format to use to highlight cells.
            worksheet = self.workbook.add_worksheet(worksheet_name)
            self._write_headers(worksheet, row_offset=2)
            for digitalisat in search_result.resultList:
                self._write_data(worksheet, digitalisat)

            self._write_filter_info(worksheet)
            worksheet.autofit()
        finally:
            self.workbook.close()
            self._workbook = None

