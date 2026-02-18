import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def test_whatsapp():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    if not tokens:
        print("❌ No se encontró el cliente 1")
        return

    token, phone_id = tokens
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": "523123173431", # Número del usuario
        "type": "text",
        "text": {"body": "🤖 Prueba de conexión interna..."}
    }
    
    print(f"Probando envío a {phone_id}...")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    test_whatsapp()
