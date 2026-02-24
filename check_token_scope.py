import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = "EAAoC7oYRllsBQ2kZAdyeLTW2y0AlIuFsWT5DjYwvs4MlpQbrWfcsJcGTDPK3ZAl4s0GLsPFJ7IIdx2vKsEOyjb4M7wGOv8X7TNvoVrhWId7uZC3Mgatr8DQf3wLXaQyhZB4YOO3J8DGfzmieSSrkzFA4oYPleTT7A6ZBhTrLntZACZBtUPbr7NJjZBgbFbRQNVL8GKv4deFbZAZAg3Otv41CtFnh2LvJmwee7BoenI8Wf33M9E65ZBVB1A92JtlQC5xRdVBGqbOPmDhJEO3QbAmg6ESZBKwZD"
# We'll also check the specific ID the user provided
TARGET_ID = "980996958435648"

def debug_permissions():
    print("--- 🔍 DIAGNÓSTICO DE TOKEN Y PERMISOS ---")
    
    # 1. Check Token Info
    url_debug = f"https://graph.facebook.com/debug_token?input_token={TOKEN}&access_token={TOKEN}"
    try:
        r = requests.get(url_debug).json()
        data = r.get('data', {})
        print(f"✅ Token válido: {data.get('is_valid', False)}")
        print(f"📅 Expira: {data.get('expires_at', 'N/A')}")
        print(f"🔑 Permisos: {', '.join(data.get('scopes', []))}")
        print(f"📱 App ID: {data.get('application', 'N/A')}")
    except Exception as e:
        print(f"❌ Error verificando token: {e}")

    # 2. List WhatsApp Business Accounts (WABAs)
    print("\n--- 📂 CUENTAS DE WHATSAPP BUSINESS DISPONIBLES ---")
    url_wabas = "https://graph.facebook.com/v22.0/me/whatsapp_business_accounts"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        r = requests.get(url_wabas, headers=headers).json()
        wabas = r.get('data', [])
        if not wabas:
            print("⚠️ No se encontraron WABAs vinculadas a este token.")
        for waba in wabas:
            print(f"🔹 WABA Name: {waba.get('name')} | ID: {waba.get('id')}")
            
            # 3. For each WABA, list Phone Numbers
            url_phones = f"https://graph.facebook.com/v22.0/{waba.get('id')}/phone_numbers"
            rp = requests.get(url_phones, headers=headers).json()
            phones = rp.get('data', [])
            for p in phones:
                is_target = " ⭐ (COINCIDE)" if p.get('id') == TARGET_ID else ""
                print(f"   ∟ 📞 Número: {p.get('display_phone_number')} | ID: {p.get('id')}{is_target}")
    except Exception as e:
        print(f"❌ Error listando cuentas: {e}")

    # 4. Direct check on the target ID
    print(f"\n--- 🎯 VERIFICACIÓN DIRECTA DEL ID: {TARGET_ID} ---")
    url_target = f"https://graph.facebook.com/v22.0/{TARGET_ID}"
    r = requests.get(url_target, headers=headers).json()
    if "error" in r:
        print(f"❌ ERROR: {r['error']['message']} (Subcode: {r['error'].get('error_subcode')})")
    else:
        print(f"✅ ÉXITO: El ID es visible. Nombre: {r.get('verified_name')}")

if __name__ == "__main__":
    debug_permissions()
