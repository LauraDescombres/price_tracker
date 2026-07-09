from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.produit_repository import get_all_products, add_product, delete_product
from app.releve_repository import get_last_price

bp = Blueprint('main', __name__)

@bp.route("/")
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

@bp.route("/ajouter", methods=['GET', 'POST'])
def ajouter():
        if request.method == 'POST':
            result = request.form

            nom = result['nom']
            url = result['url']
            cible = result['cible']

            if nom == '':
                flash('Le nom ne doit pas être vide', 'error')
                return redirect(url_for('main.ajouter'))

            if url == '':
                flash("L'url ne doit pas être vide", 'error')
                return redirect(url_for('main.ajouter'))

            if cible == '':
                cible = None
            else:
                try:
                    cible = float(cible)
                except ValueError:
                    flash('La cible doit être un nombre', 'error')
                    return redirect(url_for('main.ajouter'))

            add_product(nom, url, cible)
            return redirect(url_for('main.index'))

        return render_template("ajouter.html")

@bp.route("/supprimer/<int:id>", methods=['POST'])
def supprimer(id):
    delete = delete_product(id)

    if delete is None:
        flash('Erreur SQL', 'error')
    elif delete:
        flash('Suppression OK', 'success')
    else:
        flash('Produit introuvable', 'error')

    return redirect(url_for('main.index'))
