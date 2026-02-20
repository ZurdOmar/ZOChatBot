import requests
import os
from dotenv import load_dotenv

load_dotenv()

def debug_meta():
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("PHONE_NUMBER_ID")
    
    print(f"--- DEBUG META ---")
    print(f"Phone ID: {phone_id}")
    print(f"Token (First 20 chars): {token[:20]}...")
    
    # 1. Check Token Info
    debug_url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}"
    # Note: Using the same token as access_token only works if it's an app-level token, 
    # but we can try just checking the ID directly.
    
    # 2. Try to GET Phone ID details
    url = f"https://graph.facebook.com/v22.0/{phone_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\nConsultando detalles del Phone ID...")
    res = requests.get(url, headers=headers)
    print(f"STATUS: {res.status_code}")
    print(f"RESPONSE: {res.text}")
    
    # 3. Try to list associated numbers for the account
    # We need the WABA ID for this. From screenshot it was 1429198792139187
    waba_id = "1429198792139187"
    url_account = f"https://graph.facebook.com/v22.0/{waba_id}"
    url_numbers = f"https://graph.facebook.com/v22.0/{waba_id}/phone_numbers"
    
    print(f"\nConsultando detalles de la cuenta {waba_id}...")
    res_acc = requests.get(url_account, headers=headers)
    print(f"STATUS: {res_acc.status_code}")
    print(f"RESPONSE: {res_acc.text}")

    print(f"\nListando números de la cuenta {waba_id}...")
    res_nums = requests.get(url_numbers, headers=headers)
    print(f"STATUS: {res_nums.status_code}")
    print(f"RESPONSE: {res_nums.text}")

if __name__ == "__main__":
    debug_meta()
