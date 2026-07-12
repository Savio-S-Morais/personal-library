import os
from dotenv import load_dotenv
import unittest
from unittest.mock import patch

class TestAutorCadastrar(unittest.TestCase):
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
        self.app.config["LOGIN_DISABLED"] = True
        self.client = self.app.test_client()
        
    def tearDown(self):
        self.env.stop()

    @patch('app.routes.cadastrar.salvar_registro') 
    def test_cadastrar_autor(self, mock_cadastrar_autor):
        # Setup: Simula que o serviço funcionou
        mock_cadastrar_autor.return_value = (True, 1)
                
        response = self.client.post(
            "/cadastrar/autor",
            data={
                "nome_autor": "Eichiro Oda"
            }
        )

        # HTTP 302 significa redirecionamento temporario de página
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/cadastrar/autor")
        mock_cadastrar_autor.assert_called_once_with(
            "autor",
            { "nome_autor": "Eichiro Oda" }
        )
        
    @patch("app.routes.cadastrar.salvar_registro")
    def test_evitar_duplicidade_autor(self, mock_salvar_autor):
        # Simula que o serviço detectou um autor duplicado
        mock_salvar_autor.return_value = (
            False,
            "Autor(a) já cadastrado(a)"
        )

        response = self.client.post(
            "/cadastrar/autor",
            data={"nome_autor": "Eichiro Oda"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        mock_salvar_autor.assert_called_once_with(
            "autor",
            {"nome_autor": "Eichiro Oda" }
        )
        
        self.assertIn(
            b"Autor(a) j\xc3\xa1 cadastrado(a)",
            response.data,
        )
