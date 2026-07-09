from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
from app.services.user_service import buscar_usuario_por_nome, salvar_usuario
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

def hash(txt):
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        
        user_data = buscar_usuario_por_nome(username)
        
        if user_data and user_data['password'] == hash(password):
            user = Usuario(id=user_data['username'], nome=user_data['username'])
            login_user(user)
            return redirect(url_for('main.home'))
        
        flash("Usuário ou senha incorretos")
        
    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))