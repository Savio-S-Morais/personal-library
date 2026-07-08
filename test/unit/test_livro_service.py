import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.livro_service import adicionar_livro, obter_opcoes_selecao

class TestLivroService(unittest.TestCase):
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_obter_opcoes_selecao_autor(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'id_autor': 1, 'nomeAutor': 'Eichiro Oda'},
            {'id_autor': 2, 'nomeAutor': 'Clarice Lispector'}
        ]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        opcoes = obter_opcoes_selecao("Autor")
        
        self.assertEqual(opcoes, ['Eichiro Oda', 'Clarice Lispector'])
        mock_verificar_planilha_de_trabalho.assert_called_with("Autor")
        
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_obter_opcoes_selecao_editora(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'id_editora': 1, 'nomeEditora': 'Panini'},
            {'id_editora': 2, 'nomeEditora': 'DarkSide'}
        ]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        opcoes = obter_opcoes_selecao("Editora")
        
        self.assertEqual(opcoes, ['Panini', 'DarkSide'])
        mock_verificar_planilha_de_trabalho.assert_called_with("Editora")
        
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_obter_opcoes_selecao_acervo(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = [
            {'id_acervo': 1, 'nomeAcervo': 'Acervo Pessoal'},
            {'id_acervo': 2, 'nomeAcervo': 'Acervo Publico'}
        ]
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        opcoes = obter_opcoes_selecao("Acervo")
        
        self.assertEqual(opcoes, ['Acervo Pessoal', 'Acervo Publico'])
        mock_verificar_planilha_de_trabalho.assert_called_with("Acervo")    
    
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_adicionar_livro_com_status_invalido(self, mock_verificar_planilha_de_trabalho)  :
        dados = {'status': 'Lido', 'anoPublicacao': '2026'}
        sucesso, mensagem = adicionar_livro(dados)
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Status inválido")
        
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_adicionar_livro_ano_negativo(self, mock_verificar_planilha_de_trabalho):
        dados = {'anoPublicacao': '-1990', 'status': 'Disponível'}
        sucesso, mensagem = adicionar_livro(dados)
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "O ano não pode ser negativo")
    
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_adicionar_livro_ano_futuro(self, mock_verificar_planilha_de_trabalho):
        ano_atual = datetime.now().year
        dados = {'anoPublicacao': '5200', 'status': 'Disponível'}
        sucesso, mensagem = adicionar_livro(dados)
        self.assertFalse(sucesso)
        self.assertEqual(f"O ano não pode ser maior que {ano_atual}", mensagem)
        
    @patch('app.services.livro_service.verificar_planilha_de_trabalho')
    def test_adicionar_livro_sucesso(self, mock_verificar_planilha_de_trabalho):
        mock_sheet = MagicMock()
        dados_mock = [
            {'id_livro': 1, 'titulo': 'One Piece'}
        ]     
        mock_sheet.get_all_records.return_value = dados_mock
        mock_verificar_planilha_de_trabalho.return_value = mock_sheet
        
        dados = {
            'titulo': 'One Piece vol. 100', 'anoPublicacao': '2025', 'ISBN': '123',
            'status': 'Disponível', 'autor': 'Eichiro Oda', 'editora': 'Panini', 'acervo': 'Acervo Pessoal'
        }
        
        sucesso, novo_id = adicionar_livro(dados)
        
        self.assertTrue(sucesso)
        self.assertEqual(novo_id, 2)
        mock_sheet.append_row.assert_called()