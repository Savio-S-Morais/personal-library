from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_editora(nome_editora):
    nome_tratado = nome_editora.strip()
    if not nome_tratado:
        return False, "O nome da editora não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Editora")
    registros = sheet.get_all_records()
    
    for row in registros:
        if row['nomeEditora'].lower() == nome_editora.lower():
            return False, "Editora já cadastrada"
        
    id = [int(r['id_editora']) for r in registros if r['id_editora']]
    novo_id = max(id) + 1 if id else 1
    
    sheet.append_row([novo_id, nome_tratado])
    return True, novo_id