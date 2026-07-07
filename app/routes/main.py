from flask import Blueprint, render_template
from ..services.api_planilhas import verificar_planilha_de_trabalho
from markupsafe import escape

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/app/static')

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route('/salvar', methods=['GET', 'POST'])
def save_data():
    sheet = verificar_planilha_de_trabalho("Livro")
    # Exemplo de escrita
    sheet.append_row(["Dado 1", "Dado 2"])
    
    # Exemplo de leitura
    data = sheet.get_all_records()
    
    return {"status": "success", "data": data}

@main_bp.route("/<string:url>")
def error(url):
    url = escape(url)
    return f"Foi mal, mas a págica <i>'{url}'</i> não existe", 400