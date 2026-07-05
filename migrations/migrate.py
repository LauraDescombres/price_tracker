from app.db import connexion

try:
    with connexion() as conn:
        cursor = conn.execute("PRAGMA table_info(produits);")
        colonnes = [colonne[1] for colonne in cursor.fetchall()]

        if "prix_cible" not in colonnes:
            conn.execute("""
                ALTER TABLE produits
                ADD COLUMN prix_cible REAL;
            """)
            print("Migration effectuée.")
        else:
            print("Colonne déjà présente, rien à faire.")

except Exception as e:
    print(f"Erreur lors de la migration : {e}")