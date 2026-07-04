from flask import Blueprint, render_template
from markupsafe import escape

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/app/static')

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/<string:url>")
def error(url):
    url = escape(url)
    return f"Sorry, but the page <i>'{url}'</i> doesn't exit", 400