from datetime import datetime
from functools import lru_cache # Adiciona cache para evitar chamadas repetitivas à API
from app.services.api_planilhas import verificar_planilha_de_trabalho

@lru_cache(maxsize=128)
def obter_opcoes_selecao(aba_nome):
    # Busca dados e armazena em cache até que o cache seja limpo manualmente
    sheet = verificar_planilha_de_trabalho(aba_nome)
    registros = sheet.get_all_records()
    if not registros:
        return []
    
    # Pega a chave da segunda coluna dinamicamente
    coluna_nome = list(registros[0].keys())[1]
    return [r[coluna_nome] for r in registros]

def limpar_cache_opcoes():
    # Chame esta função quando adicionar um novo autor/editora/acervo
    obter_opcoes_selecao.cache_clear()

def adicionar_livro(dados):
    sheet = verificar_planilha_de_trabalho("Livro")
    registros = sheet.get_all_records()   
    
    status_permitidos = ["Disponível", "Em leitura", "Emprestado", "Desaparecido"]
    if dados['status'] not in status_permitidos:
        return False, "Status inválido"
    
    try:
        ano = int(dados['anoPublicacao'])
        ano_atual = datetime.now().year
        if ano < 0:
            return False, "O ano não pode ser negativo"
        if ano > ano_atual:
            return False, f"O ano não pode ser maior que {ano_atual}"
    except (ValueError, TypeError):
        return False, "O ano deve ser um número válido"
    
    
    if not registros:
        novo_id = 1
    else:
        id = [int(r.get('id_livro', 0)) for r in registros if str(r.get('id_livro', 0)).isdigit()]
        novo_id = max(id) + 1 if id else 1
    
    novo_registro = [
        novo_id, dados['titulo'], ano, dados['ISBN'], dados['status'], dados['autor'], dados['editora'], dados['acervo']
    ]
    sheet.append_row(novo_registro)
      
    return True, novo_id
