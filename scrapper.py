import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime as dt

def connexion():
    return sqlite3.connect('BDD.db')

def create_table():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''CREATE TABLE IF NOT EXISTS Releves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prix FLOAT,
            date_releve DATETIME
            );'''
            cursor.execute(sql)
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de la creation de la table: {e}")

#scrape + retourne prix
def fetch_price(url):
    try:
        page = requests.get(url)
        page.encoding = 'utf-8'

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')

            price_element = soup.select_one('.price_color')
            
            if price_element is None:
                print("Erreur : élément prix introuvable")
                return None
            else:
                price = price_element.text.lstrip('£')
                return float(price)
        else:
            print("Erreur : Page introuvable")
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

#sauvegarde
def save(price):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO Releves (prix, date_releve) VALUES (?, ?);'
            cursor.execute(sql, (price, dt.now().isoformat()))
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table: {e}")
        return None

if __name__ == '__main__':
    book_url = "https://books.toscrape.com/catalogue/soumission_998/index.html"
    create_table()
    price = fetch_price(book_url)
    if price is not None:
        save(price)