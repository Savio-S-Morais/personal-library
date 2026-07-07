from app.services.api_planilhas import verificar_planilha_de_trabalho

def adicionar_autor(nome_autor):
    # Tratamento inicial
    nome_tratado = nome_autor.strip()
    if not nome_tratado:
        return False, "O nome do autor não pode estar vazio."
    
    sheet = verificar_planilha_de_trabalho("Autor")
    registros = sheet.get_all_records()
    
    # Validação de duplicidade
    for row in registros:
        if row['nomeAutor'].lower() == nome_autor.lower():
            return False, "Autor(a) já cadastrado(a)"
        
    # Geração de ID
    id = [int(r['id_autor']) for r in registros if r['id_autor']]
    novo_id = max(id) + 1 if id else 1
        
    sheet.append_row([novo_id, nome_tratado])
    return True, novo_id