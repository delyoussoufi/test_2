from abc import abstractmethod
from io import BytesIO
from typing import List, Union, Optional

import xlsxwriter
from xlsxwriter.worksheet import Worksheet


class ExcelBaseWriter:

    def __init__(self, excel_file_path: Union[BytesIO, str]):
        self._excel_file_path = excel_file_path
        self.headers: List[str] = []
        self._workbook: Optional[xlsxwriter.Workbook] = xlsxwriter.Workbook(self._excel_file_path)

        self.header_format = self.workbook.add_format({'bold': True, 'font_size': 14, 'font_color': "black"})
        self.data_format = self.workbook.add_format({'bold': False, 'font_size': 12, 'font_color': "black"})
        self._current_row = 0

    def __del__(self):
        if self._workbook is not None:
            self._workbook.close()

    @property
    def workbook(self):
        return self._workbook

    def _write_headers(self, worksheet: Worksheet, row_offset: int = 0):
        self._current_row = row_offset
        for i, header in enumerate(self.headers):
            worksheet.write(self._current_row, i, header, self.header_format)
        self._current_row += 1

    @abstractmethod
    def export(self, *args, **kwargs):
        raise NotImplementedError("You must implement this method")
