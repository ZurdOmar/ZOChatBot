import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def check_app_status():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token = tokens[0]
    app_id = "2817973241878107"
    url = f"https://graph.facebook.com/v22.0/{app_id}?fields=name,app_type,id"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Consultando estado de la APP ID: {app_id}")
    response = requests.get(url, headers=headers)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    check_app_status()
