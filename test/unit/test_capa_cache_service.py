import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.services.capa_cache_service import carregar_cache, obter_do_cache, salvar_cache, pode_tentar_novamente, obter_aba_cache

class TestCapaCacheService(unittest.TestCase):
    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True
        self.client = self.app.test_client()
    
    # Testes carregar_cache()        
    @patch('app.services.capa_cache_service.verificar_planilha_de_trabalho')
    def test_carregar_cache_vazio(self, mock_verificar):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = []
        mock_verificar.return_value = mock_sheet
        cache = carregar_cache()
        self.assertEqual(cache, {})
      
    @patch('app.services.capa_cache_service.verificar_planilha_de_trabalho')    
    def test_carregar_cache_com_registro(self, mock_verificar):
        registro = [
            {
                "ISBN": "978857888",
                "url_capa": "...",
                "fonte": "OpenLibrary",
                "status": "SUCCESS",
                "atualizado_em": "...", 
                "tentar_novamente_em": ""
            }
        ]
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = registro
        mock_verificar.return_value = mock_sheet
        cache = carregar_cache()
        
        self.assertTrue(cache["978857888"])
        self.assertEqual(cache["978857888"]["status"], "SUCCESS")
     
    @patch('app.services.capa_cache_service.verificar_planilha_de_trabalho')     
    def test_carregar_cache_ignorando_isbn_vazio(self, mock_verficar):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [{
            "ISBN": "",
            "url_capa": "..."
        }]
        mock_verficar.return_value = mock_sheet
        cache = carregar_cache()
        self.assertEqual(cache, {})    
    
    # Testes obter_do_cache()
    def test_obter_do_cache(self):
        cache = {"123": {"status": "SUCCESS"}}
        self.assertEqual(obter_do_cache(cache, "123"),{"status": "SUCCESS"})
        self.assertIsNone(obter_do_cache(cache, "999"))
        self.assertIsNone(obter_do_cache(cache, None))
    
    # Testes salvar_cache()
    @patch('app.services.capa_cache_service.datetime')
    def test_salvar_cache_salvando_os_dados(self, mock_datetime):
        # Fixando data para testes
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
                       
        cache = {}
        mock_sheet = MagicMock()
        mock_sheet.find.return_value = None
        salvar_cache(mock_sheet, cache, "123", "", "OpenLibrary", status="NOT_FOUND")
        
        mock_sheet.append_row.assert_called_once_with([
            "123",
            "",
            "OpenLibrary",
            "NOT_FOUND",
            "2026-07-12 00:00:00",
            "2026-07-27 00:00:00"
        ])
        
        mock_sheet.update.assert_not_called()
        
        
    @patch('app.services.capa_cache_service.datetime')
    def test_salvar_cache_atualizando_dados(self, mock_datetime):
        # Fixando data para testes
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
        
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
                       
        cache = {}
        mock_sheet = MagicMock()
        mock_sheet.find.return_value = None
        salvar_cache(mock_sheet, cache, "123", "", "OpenLibrary", status="NOT_FOUND")
        
        self.assertEqual(cache["123"]["url_capa"], "")
        self.assertEqual(cache["123"]["fonte"], "OpenLibrary")
        self.assertEqual(cache["123"]["status"], "NOT_FOUND")
        self.assertEqual(cache["123"]["atualizado_em"], "2026-07-12 00:00:00")   
        
    @patch('app.services.capa_cache_service.datetime')
    def test_salvar_cache_success(self, mock_datetime):
        # Fixando data para testes
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
        
        cache = {}
        mock_sheet = MagicMock()
        mock_sheet.find.return_value = None
        salvar_cache(
            mock_sheet,
            cache,
            "123",
            "https://...",
            "OpenLibrary",
            "FOUND"
        )
        
        mock_sheet.append_row.assert_called_once()
        mock_sheet.update.assert_not_called()
        self.assertEqual(cache["123"]["status"],"FOUND")
        self.assertEqual(cache["123"]["fonte"],"OpenLibrary")
        self.assertEqual(cache["123"]["url_capa"],"https://...")
        self.assertEqual(cache["123"]["tentar_novamente_em"],"")  
        
    @patch("app.services.capa_cache_service.datetime")
    def test_salvar_cache_atualiza_registro_existente(self, mock_datetime):
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora

        cache = {
            "123": {
                "linha": 8,
                "status": "NOT_FOUND",
                "url_capa": "",
                "fonte": "NONE",
                "atualizado_em": "",
                "tentar_novamente_em": ""
            }
        }

        mock_sheet = MagicMock()
        celula = MagicMock()
        celula.row = 8
        mock_sheet.find.return_value = celula

        salvar_cache(
            mock_sheet,
            cache,
            "123",
            "https://...",
            "GoogleBooks",
            "FOUND"
        )

        mock_sheet.append_row.assert_not_called()
        mock_sheet.update.assert_called_once_with(
            "A8:F8",
            [[
                "123",
                "https://...",
                "GoogleBooks",
                "FOUND",
                "2026-07-12 00:00:00",
                ""
            ]]
        )
        self.assertEqual(cache["123"]["status"], "FOUND")
        self.assertEqual(cache["123"]["linha"], 8)      
    
    @patch('app.services.capa_cache_service.datetime')
    def test_salvar_cache_not_found_regra_15_dias(self, mock_datetime):
        # Fixando data para testes
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
        
        cache = {}
        mock_sheet = MagicMock()
        salvar_cache(mock_sheet, cache, "123", "", "", status="NOT_FOUND")
        esperado = (agora + timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(cache["123"]["tentar_novamente_em"], esperado)
        
    @patch('app.services.capa_cache_service.datetime')
    def test_salvar_cache_not_found_regra_12_horas(self, mock_datetime):
        # Fixando data para testes
        agora = datetime(2026, 7, 12)
        mock_datetime.now.return_value = agora
        
        cache = {}
        mock_sheet = MagicMock()
        salvar_cache(mock_sheet, cache, "123", "", "", status="ERROR")
        esperado = (agora + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(cache["123"]["tentar_novamente_em"], esperado)
    
    # Testes pode_tentar_novamente()
    def test_pode_tentar_novamente(self):      
        # Data Futura
        futuro = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertFalse(pode_tentar_novamente({"tentar_novamente_em": futuro}))
        
        # Data passada
        passado = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(pode_tentar_novamente({"tentar_novamente_em": passado}))
        
        # Campo vazio/inexistente
        self.assertFalse(pode_tentar_novamente({}))

    # Testes obter_aba_cache()
    @patch('app.services.capa_cache_service.verificar_planilha_de_trabalho')
    def test_obter_aba_cache_chama_corretamente(self, mock_verificar):
        obter_aba_cache()
        mock_verificar.assert_called_once_with("CacheCapas")