from app.services.api_planilhas import verificar_planilha_de_trabalho
from app.services.autor_service import adicionar_autor
from app.services.editora_service import adicionar_editora
from app.services.categoria_service import adicionar_categoria
from app.services.livro_service import adicionar_livro

def salvar_registro(tipo, dados):
    # Dicionário que mapeia o tipo para sua respectiva função de serviço
    acoes = {
        'autor': adicionar_autor,
        'editora': adicionar_editora,
        'categoria': adicionar_categoria,
        'livro': adicionar_livro
    }
    
    funcao = acoes.get(tipo)
    if funcao:
        return funcao(dados)
    return False