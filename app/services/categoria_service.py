from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_categoria(form_dados):
    # Tratamento inicial
    nome_categoria_tratado = form_dados.get("nome_categoria", "").strip()
    if not nome_categoria_tratado or not isinstance(nome_categoria_tratado, str):
        return False, "O nome da categoria não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Categoria")
    registros = sheet.get_all_records()
    
    for row in registros:
        if str(row.get('nomeCategoria', '')).lower() == nome_categoria_tratado.lower():
            return False, "Categoria já cadastrada"
        
    id = [int(r['id_categoria']) for r in registros if r['id_categoria']]
    novo_id = max(id) + 1 if id else 1
    
    sheet.append_row([novo_id, nome_categoria_tratado])
    return True, novo_id