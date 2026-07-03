import argparse
from db import connexion

def add_product(nom, url):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO produits (nom, url) VALUES (?, ?);'
            cursor.execute(sql, (nom, url))
            conn.commit()
            print(f"Produit '{nom}' ajouté.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table: {e}")
        return None


def list_products():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT id, nom, actif FROM produits'''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Erreur lors du select dans la table: {e}")
        return None

def remove_product(produit_id):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''UPDATE produits SET actif = ? WHERE id = ?;'''
            cursor.execute(sql, (0, produit_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Produit {produit_id} desactivé")
            else:
                print(f"Produit {produit_id} non trouvé")
    except Exception as e:
        print(f"Erreur lors de la desactivation dans la table: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Gestion des produits suivis")
    subparsers = parser.add_subparsers(dest="commande", required=True)

    # --- commande: add ---
    parser_add = subparsers.add_parser("add", help="Ajouter un produit")
    parser_add.add_argument("nom", help="Nom du produit")
    parser_add.add_argument("url", help="URL de la page produit")

    # --- commande: list ---
    subparsers.add_parser("list", help="Liste les produits")

    # --- commande: remove ---
    parser_remove = subparsers.add_parser("remove", help="Desactive un produit")
    parser_remove.add_argument("produit_id", help="Id du produit", type=int)

    args = parser.parse_args()

    if args.commande == "add":
        add_product(args.nom, args.url)
    elif args.commande == "list":
        produits = list_products()
        
        if produits is not None:
            for produit_id, nom, actif in produits:
                if actif == 1:
                    statut = 'actif'
                else:
                    statut = 'inactif'
                print(f"{produit_id} | {nom} | {statut}")
        else:
            print('Aucun produits')          
    elif args.commande == "remove":
        remove_product(args.produit_id)

if __name__ == "__main__":
    main()