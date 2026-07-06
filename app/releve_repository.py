from app.db import connexion

def get_last_price(produit_id):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT prix FROM releves WHERE produit_id = ? ORDER BY date_releve DESC LIMIT 1'''
            cursor.execute(sql, (produit_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return row[0]
    except Exception as e:
        print(f"Erreur lors de la récupération du dernier prix : {e}")
        return None 