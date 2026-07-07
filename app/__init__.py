from flask import Flask

def create_app():
    from .routes.main import main_bp
    from .routes.api import api_bp
    
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app