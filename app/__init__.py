from flask import Flask, render_template
from app.produit_repository import get_all_products
from app.releve_repository import get_last_price

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        produits = get_all_products()

        if produits is None:
            return render_template("produits.html", produits=[])

        produits_enrichis = [
            {"produit": p, "dernier_prix": get_last_price(p.id)}
            for p in produits
        ]
        
        return render_template("produits.html", produits=produits_enrichis)

    return app