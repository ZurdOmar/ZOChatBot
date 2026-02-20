import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def check_phone_status():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    if not tokens:
        print("❌ No se encontró el cliente 1")
        return

    token, phone_id = tokens
    # Query the phone number details
    url = f"https://graph.facebook.com/v22.0/{phone_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Consultando estado del Phone ID: {phone_id}")
    response = requests.get(url, headers=headers)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    check_phone_status()
