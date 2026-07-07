import os
import json
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR = Path(__file__).resolve().parents[2]

# Chamada de conexão reutilizavel, para evitar criar varios objetos de Credentials
_client = None

def validar_credenciais():
    global _client
    
    if _client:
        return _client
    
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

    _client = gspread.authorize(creds)
    
    return _client

def verificar_planilha_de_trabalho(sheet_name):
    conexao = validar_credenciais()
    planilha_id = os.getenv("SPREADSHEET_ID")

    if not planilha_id:
        raise RuntimeError("SPREADSHEET_ID environment variable is not defined")
    
    planilha = conexao.open_by_key(planilha_id)
    return planilha.worksheet(sheet_name)

def selecionar_valor_celula(sheet_name, cells_range):
    conexao = validar_credenciais()
    planilha_id = os.getenv("SPREADSHEET_ID")

    if not planilha_id:
        raise RuntimeError("SPREADSHEET_ID environment variable is not defined")
    
    planilha = conexao.open_by_key(planilha_id)
    
    valores = planilha.worksheet(sheet_name).get(cells_range)
    
    if not valores:
        return None
    
    if len(valores) == 1 and len(valores[0]) == 1:
        return valores[0][0]
    
    return valores