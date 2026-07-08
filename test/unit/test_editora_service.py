import unittest
from unittest.mock import patch, MagicMock
from app.services.editora_service import adicionar_editora

class TestEditoraService(unittest.TestCase):
    @patch('app.services.editora_service.verificar_planilha_de_trabalho')
    def test_evitar_duplicididade(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [{'id_editora': 1, 'nomeEditora': 'Panini'}]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        sucesso, mensagem = adicionar_editora('Panini')
        
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Editora já cadastrada")
        mock_sheet.append_row.assert_not_called()
        
    @patch('app.services.editora_service.verificar_planilha_de_trabalho')
    def test_gerar_id_incrementado(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'id_editora': 1, 'nomeEditora': 'Editora 1'},
            {'id_editora': 2, 'nomeEditora': 'Editora 2'}
        ]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        sucesso, novo_id = adicionar_editora("Nova Editora")
        
        self.assertTrue(sucesso)
        self.assertEqual(novo_id, 3)
        mock_sheet.append_row.assert_called_with([3,"Nova Editora"])