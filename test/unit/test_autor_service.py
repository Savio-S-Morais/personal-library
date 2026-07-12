import unittest
from unittest.mock import patch, MagicMock
from app.services.autor_service import adicionar_autor

class TestAutorService(unittest.TestCase):
    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['LOGIN_DISABLED'] = True
        self.client = self.app.test_client()
        
    @patch('app.services.autor_service.verificar_planilha_de_trabalho')
    def test_evitar_duplicidade(self, mock_verificar_planilha_de_trabalho):
        # Setup: Mock para retornar um autor já existente
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [{'id_autor': 1, 'nomeAutor': 'Eichiro Oda'}]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        sucesso, mensagem = adicionar_autor(
            { "nome_autor": "Eichiro Oda"}
        )
        
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Autor(a) já cadastrado(a)")
        mock_sheet.append_row.assert_not_called()

    @patch('app.services.autor_service.verificar_planilha_de_trabalho')
    def test_gerar_id_incrementado(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        # Simula 2 registros, deve gerar ID 3
        mock_sheet.get_all_records.return_value = [
            {'id_autor': 1, 'nomeAutor': 'Autor 1'},
            {'id_autor': 2, 'nomeAutor': 'Autor 2'}
        ]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        sucesso, novo_id = adicionar_autor(
            { "nome_autor": "Novo Autor"}
        )
        
        self.assertTrue(sucesso)
        self.assertEqual(novo_id, 3)
        # Verifica se chamou append_row com os dados corretos
        mock_sheet.append_row.assert_called_with([3, 'Novo Autor'])