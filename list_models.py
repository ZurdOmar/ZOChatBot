from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("--- Modelos Disponibles ---")
try:
    for model in client.models.list():
        print(f"Name: {model.name}")
except Exception as e:
    print(f"Error: {e}")
