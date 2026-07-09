from flask import Blueprint, render_template
from markupsafe import escape
from ..services.api_planilhas import verificar_planilha_de_trabalho
from ..services.livro_service import obter_todos_os_livros

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/app/static')

@main_bp.route("/")
def home():
    livros = obter_todos_os_livros()
    total_livros = len(livros)
    meta = 1000
    falta = max(0, meta - total_livros)
    progresso = (total_livros/meta) * 100
    
    return render_template('home.html',
                           livros=livros,
                           total=total_livros,
                           falta=falta,
                           progresso=progresso)

@main_bp.route("/acervo/<string:nomeAcervo>")
def listar_acervo(nomeAcervo):
    todos = obter_todos_os_livros()
    livros_filtrados = [l for l in todos if l['acervo'] == nomeAcervo]
    
    # Usa-se o show_meta=False para esconder o contador de meta da tela
    return render_template('home.html',
                           livros=livros_filtrados,
                           header_text=f"Bem-vindo ao acervo {nomeAcervo}",
                           show_meta=False)


@main_bp.route("/<string:url>")
def error(url):
    url = escape(url)
    return f"Foi mal, mas a págica <i>'{url}'</i> não existe", 400