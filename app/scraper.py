from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
from app.notifications import send_notification
from app.db import connexion
from app.produit_repository import get_active_products

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

def main():
    produits = get_active_products()
    if produits is None:
        return
        
    if not produits:
        print("Aucun produit à scraper")
        return
    
    for produit in produits:
        price = fetch_price(produit.url)
        if price is not None:
            save(price, produit.id)
            if produit.prix_cible is not None and price <= produit.prix_cible:
                message = f"🔔 ALERTE : {produit.nom} à {price} (cible : {produit.prix_cible})"
                print(message)
                send_notification(message)
            else:
                print(f"{produit.nom} : {price}")
        else:
            print(f"Erreur sur le produit {produit.nom}")

if __name__ == '__main__':
    main()