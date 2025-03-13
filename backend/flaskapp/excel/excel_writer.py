"""
Class to write data into an excel sheet.
"""
import xlsxwriter
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet


class ExcelWriter:

    @staticmethod
    def write_excel(path, sheet_name: str, headers: [str], data: []):
        """
         Write an Excel file.
        :param path: the path to save the file.
        :param sheet_name: the name of your sheet.
        :param headers: An array of string contain the headers name, .ie ("Name", "ID", "Phone").
        :param data: The data to write, it should be a List of CellValues. Each CellValues in the list
        will correspond to a row. The CellValues must have the same length as the headers.
        :return:
        """
        # Create a Workbook
        workbook = xlsxwriter.Workbook(path)

        # Create a Font for styling header cells
        header_format: Format = workbook.add_format()
        header_format.set_bold(True)
        header_format.set_font_size(14)
        header_format.set_font_color("black")

        # Create a Sheet
        worksheet: Worksheet = workbook.add_worksheet(sheet_name)

        for i in range(len(headers)):
            worksheet.write(0, i, headers[i], header_format)

        fail_format: Format = workbook.add_format()
        fail_format.set_font_color("red")

        # Create other rows.
        if data:  # if false document is empty.
            for j, row in enumerate(data):
                for i in range(len(headers)):
                    if row[i] is not None:
                        worksheet.write(j + 1, i, row[i])

        # Adjust the column width
        # row_width = []
        # for i in range(len(headers)):
        #     max_value = ExcelWriter.__excel_string_width(headers[i])
        #     for row in data:
        #         if row[i] is not None:
        #             max_value = max(max_value, ExcelWriter.__excel_string_width(row[i]))
        #     row_width.append(max_value)
        # for i in range(len(row_width)):
        #     worksheet.set_column(i, i, row_width[i])

        worksheet.autofit()
        # Write the output to a file
        workbook.close()

    @staticmethod
    def __excel_string_width(value):
        """
        Calculate the length of the string in Excel character units. This is only
        an example and won't give accurate results. It will need to be replaced
        by something more rigorous.
        """
        string_width = len(str(value))
        if string_width == 0:
            return 0
        else:
            return string_width * 1.1
