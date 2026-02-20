import requests
import sqlite3
import os
import json
from dotenv import load_dotenv

load_dotenv()

def list_template_names():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token = tokens[0]
    waba_id = "1429198792139187"
    url = f"https://graph.facebook.com/v22.0/{waba_id}/message_templates"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    print("Plantillas disponibles:")
    for template in data.get('data', []):
        print(f"- {template['name']} ({template['language']}) - Status: {template['status']}")

if __name__ == "__main__":
    list_template_names()
