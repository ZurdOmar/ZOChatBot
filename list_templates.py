import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def list_templates():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    if not tokens:
        print("❌ No se encontró el cliente 1")
        return

    token = tokens[0]
    waba_id = "1429198792139187"
    url = f"https://graph.facebook.com/v22.0/{waba_id}/message_templates"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Listando plantillas para WABA: {waba_id}")
    response = requests.get(url, headers=headers)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    list_templates()
