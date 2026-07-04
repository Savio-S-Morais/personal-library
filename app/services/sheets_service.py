import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


BASE_DIR = Path(__file__).resolve().parents[2]


def get_sheet_cliente():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    env = os.getenv("FLASK_ENV", "development")
    creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH") if env == "development" else os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
    if not creds_path:
        raise RuntimeError("GOOGLE_SHEETS_CREDENTIALS_PATH environment variable is not defined")

    full_creds_path = (BASE_DIR / creds_path).resolve() if not Path(creds_path).is_absolute() else Path(creds_path)
    if not full_creds_path.exists():
        raise FileNotFoundError(f"Credentials file not found: {full_creds_path}")

    creds = Credentials.from_service_account_file(str(full_creds_path), scopes=scopes)
    return gspread.authorize(creds)


def get_worksheet(sheet_name):
    client = get_sheet_cliente()

    env = os.getenv("FLASK_ENV", "development")
    spreadsheet_id = os.getenv("SPREADSHEET_ID") if env == "development" else os.getenv("SPREADSHEET_ID")
    if not spreadsheet_id:
        raise RuntimeError("Spreadsheet ID environment variable is not defined")

    spreadsheet = client.open_by_key(spreadsheet_id)
    return spreadsheet.worksheet(sheet_name)