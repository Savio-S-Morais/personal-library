import os
from dotenv import load_dotenv
import unittest
from unittest.mock import patch, MagicMock
from app.services.livro_categoria_service import vincular_livro_categoria
from app.services import livro_categoria_service

class TestLivroCategoriaService(unittest.TestCase):
    def setUp(self):
        load_dotenv(".env.test", override=True)
        
        self.env = patch.dict(
            os.environ,
            {
                "GOOGLE_SHEETS_CREDENTIALS_PATH": os.environ.get('GOOGLE_SHEETS_CREDENTIALS_PATH'),
                "SPREADSHEET_ID": os.environ.get('SPREADSHEET_ID'),
                "SECRET_KEY": os.environ.get('SECRET_KEY')
            }
        )
        self.env.start()
        
        self.mock_verificar_planilha_de_trabalho = patch('app.services.livro_categoria_service.verificar_planilha_de_trabalho')
        self.mock_sheet = MagicMock()
        self.mock_verificar_planilha_de_trabalho.return_values = self.mock_sheet
        
    def tearDown(self):
        patch.stopall() 
        self.env.stop()   
    
    def test_vincular_livro_categoria(self):
        with patch.object(livro_categoria_service, 'verificar_planilha_de_trabalho') as mock_method:
            mock_method.return_value = self.mock_sheet
            id_livro = 10
            id_categoria = 5
            sucesso = vincular_livro_categoria(id_livro, id_categoria)
            self.assertTrue(sucesso)
            self.mock_sheet.append_row.assert_called()
        
        self.mock_sheet.append_row.assert_called_with([id_livro, id_categoria])
        
    def test_vincular_multiplas_categorias(self):
        with patch.object(livro_categoria_service, 'verificar_planilha_de_trabalho') as mock_method:                    
            mock_method.return_value = self.mock_sheet      
            id_livro = 10
            categorias = [1,2,3]
        
            for categoria in categorias:
                vincular_livro_categoria(id_livro, categoria)
            
        self.assertEqual(self.mock_sheet.append_row.call_count, 3)
        self.mock_sheet.append_row.assert_called_with([10,3])