from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-002", "gemini-2.0-flash"]

for model_id in models_to_try:
    print(f"--- Probando {model_id} ---")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Hola, responde con solo la palabra EXITO"
        )
        print(f"Respuesta de {model_id}: {response.text}")
        break
    except Exception as e:
        print(f"Error con {model_id}: {e}")
