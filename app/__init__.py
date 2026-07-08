import os
from dotenv import load_dotenv
from flask import Flask
from app.services.livro_service import obter_opcoes_selecao

def create_app():
    if os.getenv("FLASK_ENV") == "development":
        load_dotenv(".env.development")
    
    from .routes.main import main_bp
    from .routes.api import api_bp
    from .routes.cadastrar import cadastrar_bp
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(cadastrar_bp)
    
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

    return app
