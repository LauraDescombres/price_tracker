import argparse
from app.repository import add_product, remove_product, update_target, get_all_products

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
        produits = get_all_products()
        
        if produits is None:
            return

        if not produits:
            print("Aucun produit à lister")
            return
        
        for produit in produits:
            if produit.actif == 1:
                statut = 'actif'
            else:
                statut = 'inactif'

            if produit.prix_cible is None:
                cible = "Aucune"
            else:
                cible = produit.prix_cible   
                
            print(f"{produit.id} | {produit.nom} | {cible} | {statut}")         
    elif args.commande == "remove":
        remove_product(args.produit_id)
    elif args.commande == "set-target":
        update_target(args.produit_id, args.target)

if __name__ == "__main__":
    main()