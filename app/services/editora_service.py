from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_editora(nome_editora):
    nome_tratado = nome_editora.get('nome_editora')
    if not nome_tratado or not isinstance(nome_tratado, str):
        return False, "O nome da editora não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Editora")
    registros = sheet.get_all_records()
    
    # Validação de duplicidade
    for row in registros:
        if str(row.get('nomeEditora', '')).lower() == nome_tratado.lower():
            return False, "Editora já cadastrada"
        
    # Geração de ID
    id = [int(r['id_editora']) for r in registros if r['id_editora']]
    novo_id = max(id) + 1 if id else 1
        
    sheet.append_row([novo_id, nome_tratado])
    return True, novo_id