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

        produits_enrichis = []
        for p in produits:
            dernier_prix = get_last_price(p.id)
            sous_cible = (
                p.prix_cible is not None
                and dernier_prix is not None
                and dernier_prix <= p.prix_cible
            )
            produits_enrichis.append({
                "produit": p,
                "dernier_prix": dernier_prix,
                "sous_cible": sous_cible,
            })
        
        return render_template("produits.html", produits=produits_enrichis)

    return app