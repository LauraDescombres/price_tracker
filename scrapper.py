import requests
from bs4 import BeautifulSoup


book_url = "https://books.toscrape.com/catalogue/soumission_998/index.html"

try:
    page = requests.get(book_url)
    page.encoding = 'utf-8'

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')

        price_element = soup.select_one('.price_color')
        
        if price_element is None:
            print("Erreur element introuvable")
        else:
            price = price_element.text.lstrip('£')
            print(f"Prix actuel : {float(price)}")
    else:
        error = f"Erreur {page.status_code}"
        print(error)
except requests.exceptions.RequestException as e:
    print(e)

