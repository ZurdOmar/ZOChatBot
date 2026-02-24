from google import genai
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key: {api_key[:5]}...{api_key[-5:]}")

# Test 1: HTTP Request directly to check API activation
print("\n--- Test 1: Direct HTTP Request ---")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: SDK check
print("\n--- Test 2: SDK models.list() ---")
try:
    client = genai.Client(api_key=api_key)
    models = list(client.models.list())
    if not models:
        print("No se encontraron modelos disponibles.")
    else:
        for m in models:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error SDK: {e}")
