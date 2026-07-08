from flask import Blueprint, render_template, request, flash, redirect
from ..services.autor_service import adicionar_autor
from ..services.editora_service import adicionar_editora
from ..services.categoria_service import adicionar_categoria

cadastrar_bp = Blueprint('cadastrar', __name__, template_folder='templates', static_folder='static', static_url_path='/app/static')

@cadastrar_bp.route("/cadastrar")
def home():
    return "Home de teste apenas"

@cadastrar_bp.route("/cadastrar/autor", methods=['GET', 'POST'])
def cadastrar_autor():
    if request.method == 'POST':
        nome = request.form.get('nome_autor')
        
        sucesso, resultado = adicionar_autor(nome)
        
        if sucesso:
            flash(f"Autor(a) cadastrado com sucesso!", "success")
        else:
            flash(resultado, "danger")
            
        return redirect("/cadastrar/autor")
    
    return render_template('forms_autor.html')

@cadastrar_bp.route("/cadastrar/editora", methods=['GET', 'POST'])
def cadastrar_editora():
    if request.method == 'POST':
        nome = request.form.get('nome_editora')
        
        sucesso, resultado = adicionar_editora(nome)
        
        if sucesso:
            flash(f"Editora cadastrada com sucesso!", "success")
        else:
            flash(resultado, "danger")
            
        return redirect("/cadastrar/editora")
    
    return render_template('forms_editora.html')

@cadastrar_bp.route("/cadastrar/categoria", methods=['GET', 'POST'])
def cadastrar_categoria():
    if request.method == 'POST':
        nome = request.form.get('nome_categoria')
        
        sucesso, resultado = adicionar_categoria(nome)
        
        if sucesso:
            flash(f"Categoria cadastrada com sucesso!", "success")
        else:
            flash(resultado, "danger")
            
        return redirect("/cadastrar/categoria")
    
    return render_template('forms_categoria.html')