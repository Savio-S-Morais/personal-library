from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_editora(form_dados):
    nome_editora_tratado = form_dados.get("nome_editora", "").strip()
    if not nome_editora_tratado or not isinstance(nome_editora_tratado, str):
        return False, "O nome da editora não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Editora")
    registros = sheet.get_all_records()
    
    # Validação de duplicidade
    for row in registros:
        if str(row.get('nomeEditora', '')).lower() == nome_editora_tratado.lower():
            return False, "Editora já cadastrada"
        
    # Geração de ID
    id = [int(r['id_editora']) for r in registros if r['id_editora']]
    novo_id = max(id) + 1 if id else 1
        
    sheet.append_row([novo_id, nome_editora_tratado])
    return True, novo_id