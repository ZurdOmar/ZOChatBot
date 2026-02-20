import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def register_phone():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    if not tokens:
        print("❌ No se encontró el cliente 1")
        return

    token, phone_id = tokens
    url = f"https://graph.facebook.com/v22.0/{phone_id}/register"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "pin": "123456" # Temporary trial PIN, might need user's PIN if 2FA is on
    }
    
    print(f"Intentando REGISTRAR el Phone ID: {phone_id}")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    register_phone()
