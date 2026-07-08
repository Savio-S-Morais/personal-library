import os
from dotenv import load_dotenv
import unittest
from unittest.mock import patch

class TestEditoraCadastrar(unittest.TestCase):
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
        
    @patch('app.routes.cadastrar.adicionar_editora')
    def test_adicionar_editora(self, mock_adicionar_editora):
        mock_adicionar_editora.return_value = (True, 1)
        
        response = self.client.post(
            "/cadastrar/editora",
            data={"nome_editora": "Panini"}
        )
        
        # HTTP 302 significa redirecionamento temporario de página
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/cadastrar/editora")
        
    @patch('app.routes.cadastrar.adicionar_editora')
    def test_evitar_duplicidade_editora(self, mock_adicionar_editora):
        mock_adicionar_editora.return_value = (
            False,
            "Editora já cadastrada"
        )
        
        response = self.client.post(
            "/cadastrar/editora",
            data={"nome_editora": "Panini"},
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        mock_adicionar_editora.assert_called_once_with("Panini")
        
        self.assertIn(
            b"Editora j\xc3\xa1 cadastrada",
            response.data
        )