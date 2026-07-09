from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_categoria(nome_categoria):
    nome_tratado = nome_categoria.get('nome_categoria')
    
    if not nome_tratado or not isinstance(nome_tratado, str):
        return False, "O nome da categoria não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Categoria")
    registros = sheet.get_all_records()
    
    for row in registros:
        if str(row.get('nomeCategoria', '')).lower() == nome_tratado.lower():
            return False, "Categoria já cadastrada"
        
    id = [int(r['id_categoria']) for r in registros if r['id_categoria']]
    novo_id = max(id) + 1 if id else 1
    
    sheet.append_row([novo_id, nome_tratado])
    return True, novo_id