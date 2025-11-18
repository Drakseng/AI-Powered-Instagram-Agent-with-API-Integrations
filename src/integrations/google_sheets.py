from typing import List, Dict
import gspread
from google.oauth2.service_account import Credentials


def get_sheets_client(service_account_json: str) -> gspread.Client:
    """
    Build and return an authorized gspread client using a service account JSON file.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_file(service_account_json, scopes=scopes)
    return gspread.authorize(credentials)


def fetch_products(
    service_account_json: str,
    spreadsheet_name: str,
    worksheet_name: str,
) -> List[Dict]:
    """
    Fetch all product records from a Google Sheets worksheet.

    The sheet is expected to have column names such as:
        - 'ürün_adı'
        - 'başlık'
        - 'açıklama'
        - 'madde_işaretleri'
        - 'konu'
        - 'görsel_link'
        (plus any other fields you want to use)

    Returns:
        List of product dictionaries, one per row.
    """
    client = get_sheets_client(service_account_json)
    worksheet = client.open(spreadsheet_name).worksheet(worksheet_name)
    return worksheet.get_all_records()
