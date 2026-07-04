import requests
from db import connexion
from bs4 import BeautifulSoup
from datetime import datetime as dt
from config import WEBHOOK_URL

#fonction qui recupère les produits actifs
def get_products():
    try: 
        with connexion() as conn:
            cursor = conn.cursor()
            sql = '''SELECT id, nom, url, prix_cible FROM produits WHERE actif = 1;'''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return None

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
def save(price, produit_id):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            sql = 'INSERT INTO releves (prix, date_releve, produit_id) VALUES (?, ?, ?);'
            cursor.execute(sql, (price, dt.now().isoformat(), produit_id))
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table: {e}")
        return None
    
def send_notification(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")

def main():
    produits = get_products()
    if produits is None:
        return
        
    if not produits:
        print("Aucun produit à scraper")
        return
    
    for produit_id, nom, url, prix_cible in produits:
        price = fetch_price(url)
        if price is not None:
            save(price, produit_id)
            if prix_cible is not None and price <= prix_cible:
                if prix_cible is not None and price <= prix_cible:
                    message = f"🔔 ALERTE : {nom} à {price} (cible : {prix_cible})"
                    print(message)
                    send_notification(message)
            else:
                print(f"{nom} : {price}")
        else:
            print(f"Erreur sur le produit {nom}")

if __name__ == '__main__':
    main()