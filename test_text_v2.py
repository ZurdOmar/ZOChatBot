import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def test_text_message():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token, phone_id = tokens
    # Using the recipient from .env (5215641777085)
    recipient = os.getenv("RECIPIENT_PHONE_NUMBER")
    
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": "¡Hola Omar! Prueba FINAL al número correcto. El bot está 100% activo. 🤖🚀"
        }
    }
    
    print(f"Enviando mensaje de texto DESDE ...5877 HACIA {recipient}")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    test_text_message()
