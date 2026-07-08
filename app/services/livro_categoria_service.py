from app.services.api_planilhas import verificar_planilha_de_trabalho

def vincular_livro_categoria(id_livro, id_categoria):
    try:
        sheet = verificar_planilha_de_trabalho("LivroCategoria")
        row = [id_livro, id_categoria]
        sheet.append_row(row)
        return True
    except Exception as e:
        print(f"Erro ao vincular categorias: {e}")
        return False