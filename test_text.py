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
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": "5213351380285", # User's personal number
        "type": "text",
        "text": {
            "body": "¡Hola Omar! Soy tu bot con el nuevo Token de Sistema. 🤖🚀"
        }
    }
    
    print(f"Enviando mensaje de texto desde ...5877")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    test_text_message()
