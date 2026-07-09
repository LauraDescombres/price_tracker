import sqlite3

def connexion():
    conn = sqlite3.connect('BDD.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        url TEXT NOT NULL,
        actif INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS releves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produit_id INTEGER NOT NULL,
        prix REAL NOT NULL,
        date_releve DATETIME NOT NULL,
        FOREIGN KEY (produit_id) REFERENCES produits(id)
    );
    """

    try:
        with connexion() as conn:
            conn.executescript(sql)
            print("Base initialisée.")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")

if __name__ == '__main__':
    create_tables()