import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from app.models.usuario import Usuario
from app.services.user_service import buscar_usuario_por_nome
from app.services.livro_service import obter_opcoes_selecao

def create_app():
    if os.getenv("FLASK_ENV") == "development":
        load_dotenv(".env.development")
    
    from .routes.main import main_bp
    from .routes.api import api_bp
    from .routes.cadastrar import cadastrar_bp
    from .routes.autorizacao import auth_bp
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    @app.context_processor
    def inject_acervos():
        from app.services.livro_service import obter_todos_os_livros
        
        livros = obter_todos_os_livros()
        total = len(livros)
        meta = 1000
        progresso = (total/meta) * 100
        
        return dict(
                acervos_lista=obter_opcoes_selecao("Acervo"),
                total=total,
                progresso=progresso
            )

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
        
    @login_manager.user_loader
    def load_user(username):
        user_data = buscar_usuario_por_nome(username)
        if user_data:
            return Usuario(id=user_data['id_user'], nome=user_data['username'])
        return None
        
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(cadastrar_bp)
    app.register_blueprint(auth_bp)

    return app