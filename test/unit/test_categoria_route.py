import os
from dotenv import load_dotenv
import unittest
from unittest.mock import patch

class TestCategoriaCadastrar(unittest.TestCase):
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
        
        from app import create_app

        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def tearDown(self):
        self.env.stop()
        
    @patch('app.routes.cadastrar.cadastrar_categoria')
    def test_cadastrar_categoria(self, mock_cadastrar_categoria):
        mock_cadastrar_categoria.return_value = (True, 1)
        
        response = self.client.post(
            "/cadastrar/categoria",
            data={"nome_categoria": "Ficção"}
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/cadastrar/categoria")
    
    @patch('app.routes.cadastrar.cadastrar_categoria')    
    def test_evitar_duplicidade_editora(self, mock_cadastrar_categoria):
        mock_cadastrar_categoria.return_value = (
            False,
            "Categoria já cadastada"
        )
        
        response = self.client.post(
            "/cadastrar/categoria",
            data={"nome_categoria": "Ficção"},
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        mock_cadastrar_categoria.asset_called_once_with("Ficção")
        
        self.assertIn(
            b"Categoria j\xc3\xa1 cadastrada",
            response.data
        )