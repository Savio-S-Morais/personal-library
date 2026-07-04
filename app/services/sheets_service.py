import os
import json
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR = Path(__file__).resolve().parents[2]

def get_sheet_cliente():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    env = os.getenv("FLASK_ENV", "development")
    creds_data = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

    if not creds_data:
        raise RuntimeError("GOOGLE_SHEETS_CREDENTIALS_PATH environment variable is not defined")
    
    if creds_data.startswith("{"):
        creds_info = json.loads(creds_data)
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    else:
        full_creds_path = (BASE_DIR / creds_data).resolve()
        if not full_creds_path.exists():
            raise FileNotFoundError(f"Credentials file not found at {full_creds_path}")
        creds = Credentials.from_service_account_file(str(full_creds_path), scopes=scopes)

    return gspread.authorize(creds)

def get_worksheet(sheet_name):
    client = get_sheet_cliente()
    spreadsheet_id = os.getenv("SPREADSHEET_ID")

    if not spreadsheet_id:
        raise RuntimeError("SPREADSHEET_ID environment variable is not defined")
    
    spreadsheet = client.open_by_key(spreadsheet_id)
    return spreadsheet.worksheet(sheet_name)