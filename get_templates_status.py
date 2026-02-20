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
    
    token = tokens[0]
    waba_id = "1429198792139187"
    url = f"https://graph.facebook.com/v22.0/{waba_id}/message_templates"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Listando plantillas para WABA: {waba_id}")
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "data" in data:
        for t in data["data"]:
            print(f"NOMBRE: {t['name']} | ESTADO: {t['status']} | CATEGORIA: {t['category']} | LENGUAJE: {t['language']}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    list_templates()
