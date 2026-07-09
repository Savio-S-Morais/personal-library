from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask_login import login_required
from app.services.livro_service import obter_opcoes_selecao, adicionar_livro
from app.services.cadastro_service import salvar_registro

cadastrar_bp = Blueprint('cadastrar', __name__, template_folder='templates', static_folder='static', static_url_path='/app/static', url_prefix="/cadastrar")

@cadastrar_bp.before_request
@login_required
def require_login():
    pass

@cadastrar_bp.route("/")
def home():
    return render_template('cadastrar/cadastrar.html')

@login_required
@cadastrar_bp.route('/<tipo>', methods=['GET', 'POST'])
def formulario(tipo):
    if request.method == 'POST':
        dados = request.form.to_dict()
        
        # Tratamento especial para categorias múltiplas
        if tipo == 'livro':
            dados['categorias'] = request.form.getlist('categoria[]')
            
        if salvar_registro(tipo, dados):
            flash(f"{tipo.capitalize()} cadastrado com sucesso!", "success")
        else:
            flash(f"Erro ao cadastrar {tipo}", "danger")
            
        return redirect(url_for('cadastrar.formulario', tipo=tipo))
    
    ano_atual = { "ano_atual": datetime.now().year } 
    
    return render_template(f"cadastrar/forms_{tipo}.html", tipo=tipo, **obter_dados_auxiliares(tipo), **ano_atual)

def obter_dados_auxiliares(tipo):
    # Retorna os dados para preencher os <select> do formulário
    if tipo == 'livro':
        return {
            'autores': obter_opcoes_selecao("Autor"),
            'editoras': obter_opcoes_selecao("Editora"),
            'acervos': obter_opcoes_selecao("Acervo"),
            'categorias': obter_opcoes_selecao("Categoria")
        }
    return {}