import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from app.services.capa_service import buscar_openlibrary, buscar_google_books, obter_capa

class TestCapaService(unittest.TestCase):
    
    # Testes buscar_openlibrary()
    def test_buscar_openlibrary_success(self):
        with patch('app.services.capa_service.requests.head') as mock_head:
            mock_head.return_value.status_code = 200
            url = buscar_openlibrary("9780385533225")
            self.assertEqual(url, "https://covers.openlibrary.org/b/isbn/9780385533225-M.jpg?default=false")
            
    def test_buscar_openlibrary_nao_encontrado(self):
        with patch('app.services.capa_service.requests.head') as mock_head:
            mock_head.return_value.status_code = 404
            self.assertIsNone(buscar_openlibrary("123"))
    
    @patch("app.services.capa_service.requests.head")
    def test_busca_openlibrary_excecao(self, mock_head):
        mock_head.side_effect = RequestException()
        self.assertIsNone(buscar_openlibrary("123"))
        
    
    # Testes buscar_google_books()
    def test_buscar_google_books_sucesso_prioridade(self):
        mock_data = {
            "totalItems": 1,
            "items": [{"volumeInfo": {"imageLinks": {"extraLarge": "http://xl.jpg", "thumbnail": "http://thumb.jpg"}}}]
        }
        
        with patch('app.services.capa_service.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_data
            mock_get.return_value.status_code = 200
            resultado = buscar_google_books("123")
            self.assertEqual(resultado["status"], "FOUND")
            self.assertEqual(resultado["url"], "https://xl.jpg")
            
    def test_buscar_google_books_erros(self):
        # Resposta sem itens
        mock_data = {
            "totalItems": 1,
            "items":""
        }
        if not mock_data.get("items"):
            return None
        
        with patch('app.services.capa_service.requests.get') as mock_get:
            
            # Simula 404 (Too many request)
            mock_get.return_value.status_code = 404
            self.assertEqual(buscar_google_books("123")["status"], "NOT_FOUND")
            self.assertIsNone(buscar_google_books("123")["url"])
            
            # Simula 429 (Too many request)
            mock_get.return_value.status_code = 429
            self.assertEqual(buscar_google_books("123")["status"], "ERROR")
            self.assertIsNone(buscar_google_books("123")["url"])
            
            # Simula 500 (Too many request)
            mock_get.return_value.status_code = 500
            self.assertEqual(buscar_google_books("123")["status"], "ERROR")
            self.assertIsNone(buscar_google_books("123")["url"])
            
            # Simula erro de exceção
            mock_get.side_effect = RequestException()
            self.assertIsNone(buscar_google_books("123"))
        
    # Testes obter_capa()
    def test_obter_capa_isbn_vazio(self):
        url = obter_capa("", {}, MagicMock())
        self.assertEqual(url, "/static/img/sem_capa.jpg")
    
    @patch("app.services.capa_service.obter_do_cache")
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.buscar_google_books")
    def test_obter_capa_cache_found(self, mock_google, mock_open, mock_cache):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = {"status": "FOUND", "url_capa": "https://url.jpg"}
        
        url = obter_capa("123", cache, sheet)
        
        self.assertEqual(url, "https://url.jpg")
        mock_open.assert_not_called()
        mock_google.assert_not_called()
    
    @patch("app.services.capa_service.pode_tentar_novamente")
    @patch("app.services.capa_service.obter_do_cache")
    def test_obter_capa_cache_not_found_valido(self, mock_tentar, mock_cache):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = {"status": "NOT_FOUND"}
        mock_tentar.return_value = False
        
        url = obter_capa("123", cache, sheet)
        
        self.assertEqual(url, "/static/img/sem_capa.jpg")
    
    @patch("app.services.capa_service.obter_capa")
    @patch("app.services.capa_service.obter_do_cache")    
    def test_obter_capa_cache_error_valido(self, mock_tentar, mock_cache):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = {"status": "ERROR"}
        mock_tentar.return_value = False
        
        url = obter_capa("123", cache, sheet)
        
        self.assertEqual(url, "/static/img/sem_capa.jpg")
    
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.pode_tentar_novamente")
    @patch("app.services.capa_service.obter_do_cache") 
    def test_obter_capa_cache_expirado(self, mock_cache, mock_tentar, mock_open):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = {"status": "NOT_FOUND", "url_capa": "/static/img/sem_capa.jpg"}
        mock_tentar.return_value = True
        mock_open.return_value = "https://nova_capa.jpg"
        
        
        url = obter_capa("123", cache, sheet)
        
        mock_tentar.assert_called_once_with(mock_cache.return_value)
        mock_open.assert_called_once_with("123")
        self.assertEqual(url, "https://nova_capa.jpg")
    
    @patch("app.services.capa_service.salvar_cache")
    @patch("app.services.capa_service.obter_do_cache")
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.buscar_google_books")        
    def test_obter_capa_fluxo_open_library_encontra(self, mock_google, mock_open, mock_cache, mock_salvar):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = None
        mock_open.return_value = {"status":"FOUND", "url":"https://openlibrary.jpg"}
        mock_google.return_value = None
        
        url = obter_capa("123", cache, sheet)
        self.assertEqual(url["url"], "https://openlibrary.jpg")
        mock_salvar.assert_called_once()
        
    @patch("app.services.capa_service.salvar_cache")
    @patch("app.services.capa_service.obter_do_cache")
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.buscar_google_books")        
    def test_obter_capa_fluxo_google_encontra(self, mock_google, mock_open, mock_cache, mock_salvar):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = None
        mock_open.return_value = None
        mock_google.return_value = {"status":"FOUND", "url":"https://google.jpg"}
        
        url = obter_capa("123", cache, sheet)
        self.assertEqual(url, "https://google.jpg")
        mock_salvar.assert_called_once()
        
    @patch("app.services.capa_service.salvar_cache")
    @patch("app.services.capa_service.obter_do_cache")
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.buscar_google_books")        
    def test_obter_capa_fluxo_google_error(self, mock_google, mock_open, mock_cache, mock_salvar):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = None
        mock_open.return_value = None
        mock_google.return_value = {"status":"ERROR", "url":"/static/img/sem_capa.jpg"}
        
        url = obter_capa("123", cache, sheet)
        self.assertEqual(url, "/static/img/sem_capa.jpg")
        mock_salvar.assert_called_once()
    
    @patch("app.services.capa_service.salvar_cache")
    @patch("app.services.capa_service.obter_do_cache")
    @patch("app.services.capa_service.buscar_openlibrary")
    @patch("app.services.capa_service.buscar_google_books")        
    def test_obter_capa_nenhuma_api_encontrada(self, mock_google, mock_open, mock_cache, mock_salvar):
        cache = {}
        sheet = MagicMock()
        mock_cache.return_value = None
        mock_open.return_value = None
        mock_google.return_value = None
        
        url = obter_capa("123", cache, sheet)
        self.assertEqual(url, "/static/img/sem_capa.jpg")
        mock_salvar.assert_called_once()