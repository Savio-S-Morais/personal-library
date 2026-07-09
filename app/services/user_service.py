from app.services.api_planilhas import verificar_planilha_de_trabalho

def buscar_usuario_por_nome(username):
    sheet = verificar_planilha_de_trabalho("Usuarios")
    registros = sheet.get_all_records()
    print(f"DEBUG: Buscando usuário '{username}' em {len(registros)} registros.")
    for usuario in registros:
        if usuario['username'] == username:
            return usuario
    return None

def salvar_usuario(username, password_hash):
    sheet = verificar_planilha_de_trabalho("Usuarios")
    registros = sheet.get_all_records()
    id = [int(r['id_user']) for r in registros if r['id_user']]
    novo_id = max(id) + 1 if id else 1
    
    sheet = verificar_planilha_de_trabalho("Usuarios")
    sheet.append_row([novo_id, username, password_hash])