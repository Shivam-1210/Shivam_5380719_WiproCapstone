import openpyxl
from utils.logger import LogGen

logger = LogGen.loggen()

class ExcelReader:
    @staticmethod
    def read_excel(file_name, sheet_name):
        logger.info(f"Reading Excel file: {file_name}, sheet: {sheet_name}")

        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook[sheet_name]

        headers = [cell.value for cell in sheet[1]]
        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_dict = {}
            for idx, value in enumerate(row):
                row_dict[headers[idx]] = value
            data.append(row_dict)

        logger.info(f"Loaded {len(data)} rows from {sheet_name}")
        return data