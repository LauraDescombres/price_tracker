from flask import Flask, render_template
from app.produit_repository import get_all_products

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        produits = get_all_products()
        return render_template("produits.html", produits=produits)

    return app