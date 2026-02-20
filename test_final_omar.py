import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def test_final_delivery():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token, phone_id = tokens
    # Exact number provided by Omar
    recipient = "5213123173431"
    
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": "¡Hola Omar! Ahora sí, al número exacto corregido. ID Mensaje pronto... 🤖🚀"
        }
    }
    
    print(f"Enviando mensaje FINAL a {recipient} desde ...5877")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    test_final_delivery()
