import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def check_cert_status():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token, phone_id = tokens
    # Query certificate and name status
    url = f"https://graph.facebook.com/v22.0/{phone_id}?fields=name_status,certificate,status,new_certificate_status"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Consultando CERTIFICADO del Phone ID: {phone_id}")
    response = requests.get(url, headers=headers)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    check_cert_status()
