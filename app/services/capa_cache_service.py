from datetime import datetime, timedelta
from app.services.api_planilhas import verificar_planilha_de_trabalho

ABA_CACHE = "CacheCapas"

def carregar_cache():
    sheet = verificar_planilha_de_trabalho(ABA_CACHE)
    registros = sheet.get_all_records()
    
    cache = {}
    
    for registro in registros:
        isbn = str(registro.get("ISBN", "")).strip()
        
        if not isbn:
            continue
        
        cache[isbn] = {
            "url_capa": registro.get("url_capa"),
            "fonte": registro.get("fonte"),
            "status": registro.get("status"),
            "atualizado_em": registro.get("atualizado_em"),
            "tentar_novamente_em": registro.get("tentar_novamente_em")
        }
        
    return cache

def obter_do_cache(cache, isbn):
    if not isbn:
        return None
    
    return cache.get(str(isbn).strip())

def salvar_cache(sheet, cache, isbn, url, fonte, status):
    agora = datetime.now()
    
    if status == "NOT_FOUND":
        tentar_novamente = (
            datetime.now() + timedelta(days=15)
        ).strftime("%Y-%m-%d %H:%M:%S")
    elif status == "ERROR":
        tentar_novamente = (
            datetime.now() + timedelta(hours=12)
        ).strftime("%Y-%m-%d %H:%M:%S")
    else:
        tentar_novamente = ""
        
    atualizado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sheet.append_row([
        isbn,
        url,
        fonte,
        status,
        atualizado_em,
        tentar_novamente
    ])
    
    cache[isbn] = {
        "url_capa": url,
        "fonte": fonte,
        "status": status,
        "atualizado_em": atualizado_em,
        "tentar_novamente_em": tentar_novamente
    }
    
def obter_aba_cache():
    return verificar_planilha_de_trabalho(ABA_CACHE)

def pode_tentar_novamente(registro):
    data = registro.get("tentar_novamente_em")
    if not data:
        return False
    
    data_limite = datetime.strptime(
        data,
        "%Y-%m-%d %H:%M:%S"
    )
    
    return datetime.now() >= data_limite