import pandas as pd
import os
from utils.logger import LogGen

logger = LogGen.loggen()


def read_excel_data(sheet_name, file_path="test_data/passenger_data.xlsx"):
    try:
        # Get the absolute path to the Excel file
        base_path = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(base_path, file_path)

        logger.info(f"Reading Excel: {full_path} | Sheet: {sheet_name}")

        df = pd.read_excel(full_path, sheet_name=sheet_name)
        df = df.fillna("")  # Replace empty cells with empty strings

        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Excel Read Error: {e}")
        return []