import argparse
from app.db import connexion

def add_product(nom, url, prix_cible):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO produits (nom, url, prix_cible) VALUES (?, ?, ?);'
            cursor.execute(sql, (nom, url, prix_cible))
            conn.commit()
            print(f"Produit '{nom}' ajouté.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table: {e}")
        return None

def list_products():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT id, nom, actif, prix_cible FROM produits'''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Erreur lors du select dans la table: {e}")

def update_target(produit_id, prix_cible):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''UPDATE produits SET prix_cible = ? WHERE id = ?;'''
            cursor.execute(sql, (prix_cible, produit_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Prix cible pour le produit {produit_id} mis à jour")
            else:
                print(f"Produit {produit_id} non trouvé")
    except Exception as e:
        print(f"Erreur lors de l'update {e}")

def remove_product(produit_id):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''UPDATE produits SET actif = ? WHERE id = ?;'''
            cursor.execute(sql, (0, produit_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Produit {produit_id} désactivé")
            else:
                print(f"Produit {produit_id} non trouvé")
    except Exception as e:
        print(f"Erreur lors de la desactivation dans la table: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gestion des produits suivis")
    subparsers = parser.add_subparsers(dest="commande", required=True)

    # --- commande: add ---
    parser_add = subparsers.add_parser("add", help="Ajouter un produit")
    parser_add.add_argument("nom", help="Nom du produit")
    parser_add.add_argument("url", help="URL de la page produit")
    parser_add.add_argument("--target", type=float, default=None)

    # --- commande: list ---
    subparsers.add_parser("list", help="Liste les produits")

    # --- commande: remove ---
    parser_remove = subparsers.add_parser("remove", help="Désactive un produit")
    parser_remove.add_argument("produit_id", help="Id du produit", type=int)

    # --- commande: set-target ---
    parser_set_target = subparsers.add_parser("set-target", help="Ajoute un prix cible sur un produit existant")
    parser_set_target.add_argument("produit_id", help="Id du produit", type=int)
    parser_set_target.add_argument("target", type=float, default=None)

    args = parser.parse_args()

    if args.commande == "add":
        add_product(args.nom, args.url, args.target)
    elif args.commande == "list":
        produits = list_products()
        
        if produits is None:
            return

        if not produits:
            print("Aucun produit à lister")
            return
        
        for produit_id, nom, actif, prix_cible in produits:
            if actif == 1:
                statut = 'actif'
            else:
                statut = 'inactif'

            if prix_cible is None:
                cible = "Aucune"
            else:
                cible = prix_cible   
                
            print(f"{produit_id} | {nom} | {cible} | {statut}")         
    elif args.commande == "remove":
        remove_product(args.produit_id)
    elif args.commande == "set-target":
        update_target(args.produit_id, args.target)

if __name__ == "__main__":
    main()