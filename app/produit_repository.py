from app.db import connexion
from app.models import Produit

def get_all_products():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT id, nom, url, actif, prix_cible FROM produits'''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Produit(*row) for row in rows]
    except Exception as e:
        print(f"Erreur lors du select dans la table: {e}")
        return None

def get_active_products():
    try: 
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT id, nom, url, actif, prix_cible FROM produits WHERE actif = 1;'''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Produit(*row) for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return None 
    
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

def desactivate_product(produit_id):
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

def delete_product(produit_id):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql1 = '''DELETE FROM releves WHERE produit_id = ?;'''
            sql2 = '''DELETE FROM produits WHERE id = ?;'''
            cursor.execute(sql1, (produit_id,))
            cursor.execute(sql2, (produit_id,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la suppression d'un produit {e}")
        return None