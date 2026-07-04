# Price Tracker

Projet personnel dans le cadre de l'apprentissage de python qui a pour but de scraper le prix d'une liste de produits.
Utilisation du site https://books.toscrape.com/index.html

## Fonctionnalités

- Ajouter un produit à scraper
- Lister les produits à scraper
- Désactiver un produit à scraper
- Scraper les prix
- Alertes de prix via Discord

## Installation

```powershell
git clone https://github.com/ton-user/price_tracker.git
cd price_tracker
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python db.py
```
- copier config.example.py en config.py et y renseigner l'URL du webhook Discord 

## Utilisation

- ajouter un produit à scraper
```powershell 
python admin.py add {nom} {url}
```

- lister les produits à scraper
```powershell 
python admin.py list
```

- désactiver un produit de la liste
```powershell 
python admin.py remove {produit_id}
```

- récupérer le prix
```powershell 
python scraper.py
```


## Stack

- python 3.13+
- requests
- BeautifulSoup
- SQLite