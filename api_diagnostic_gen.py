from google import genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print(f"Probando generación con: {api_key[:5]}...{api_key[-5:]}")

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hola, responde con solo la palabra EXITO"
    )
    print(f"RESULTADO: {response.text}")
except Exception as e:
    print(f"ERROR GENERACIÓN: {e}")
