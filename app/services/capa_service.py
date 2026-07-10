import os
import requests
import time
from app.services.capa_cache_service import obter_do_cache, salvar_cache, pode_tentar_novamente

GOOGLE_BOOKS_KEY = os.getenv("API_KEY")

def buscar_openlibrary(isbn):
    url = (
        f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
    )
    
    try:
        response = requests.head(
            url,
            timeout=5,
            allow_redirects=True
        )
        
        if response.status_code == 200:
            return url
        
    except requests.RequestException:
        pass
    
    return None

def buscar_google_books(isbn):
    url = (
        "https://www.googleapis.com/books/v1/volumes"
        f"?q=isbn:{isbn}&key={GOOGLE_BOOKS_KEY}"
    )
    
    for tentativa in range(3):
            
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                
                if response.status_code in [429,500,502,503,504]:
                    time.sleep(1)
                    return {
                        "status": "ERROR",
                        "url": None
                    }
                    
                return {
                    "status": "NOT_FOUND",
                    "url": None
                }
            
            data = response.json()
                
            if not data.get("items"):
                return None
            
            volume = data["items"][0]
            
            imagens = (
                volume
                .get("volumeInfo", {})
                .get("imageLinks", {})
            )

            capa = (
                imagens.get("extraLarge")
                or imagens.get("large")
                or imagens.get("medium")
                or imagens.get("thumbnail")
                or imagens.get("smallThumbnail")
            )

            if capa:
                return capa.replace("http://", "https://")

            return None
            
        except requests.RequestException:
            return None
    
def obter_capa(isbn, cache, aba_cache):

    if not isbn:
        return "/static/img/sem_capa.jpg"

    isbn = str(isbn).strip()

    # Verifica cache existente
    registro = obter_do_cache(cache, isbn)

    if registro:

        status = registro.get("status")

        if status == "FOUND":
            return registro["url_capa"]

        if status in ["NOT_FOUND", "ERROR"]:

            if not pode_tentar_novamente(registro):
                return registro["url_capa"]


    # Tenta Open Library
    capa = buscar_openlibrary(isbn)

    if capa:

        salvar_cache(
            aba_cache,
            cache,
            isbn,
            capa,
            "OpenLibrary",
            "FOUND"
        )

        return capa


    # Tenta Google Books
    resultado_google = buscar_google_books(isbn)

    if resultado_google:

        if resultado_google["status"] == "FOUND":

            salvar_cache(
                aba_cache,
                cache,
                isbn,
                resultado_google["url"],
                "GoogleBooks",
                "FOUND"
            )

            return resultado_google["url"]


        if resultado_google["status"] == "ERROR":

            salvar_cache(
                aba_cache,
                cache,
                isbn,
                "/static/img/sem_capa.jpg",
                "GoogleBooks",
                "ERROR"
            )

            return "/static/img/sem_capa.jpg"


    # Não encontrou em nenhuma fonte
    salvar_cache(
        aba_cache,
        cache,
        isbn,
        "/static/img/sem_capa.jpg",
        "NONE",
        "NOT_FOUND"
    )

    return "/static/img/sem_capa.jpg"