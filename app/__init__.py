import os
from dotenv import load_dotenv
from flask import Flask

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

    return app