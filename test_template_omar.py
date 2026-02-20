import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def test_template_delivery():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT whatsapp_token, phone_number_id FROM clients WHERE id=1')
    tokens = cursor.fetchone()
    conn.close()
    
    token, phone_id = tokens
    recipient = "5213123173431"
    
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Template message (Initiates conversation)
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    
    print(f"Enviando PLANTILLA hello_world a {recipient} desde ...5877")
    response = requests.post(url, headers=headers, json=data)
    print(f"STATUS: {response.status_code}")
    print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    test_template_delivery()
