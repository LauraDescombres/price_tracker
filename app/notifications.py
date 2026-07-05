import requests
from app.config import WEBHOOK_URL

def send_notification(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")