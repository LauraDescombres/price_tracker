from flask import Flask, render_template, request, redirect, url_for, flash
from app.produit_repository import get_all_products, add_product
from app.releve_repository import get_last_price
from app.config import secret_key

def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key

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

    @app.route("/ajouter", methods=['GET', 'POST'])
    def ajouter():
        if request.method == 'POST':
            result = request.form

            nom = result['nom']
            url = result['url']
            cible = result['cible']

            if nom == '':
                flash('Le nom ne doit pas être vide', 'error')
                return redirect(url_for('ajouter'))

            if url == '':
                flash("L'url ne doit pas être vide", 'error')
                return redirect(url_for('ajouter'))

            if cible == '':
                cible = None
            else:
                try:
                    cible = float(cible)
                except ValueError:
                    flash('La cible doit être un nombre', 'error')
                    return redirect(url_for('ajouter'))

            add_product(nom, url, cible)
            return redirect(url_for('index'))

        return render_template("ajouter.html")

    return app