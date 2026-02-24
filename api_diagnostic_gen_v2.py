from google import genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = ["gemini-1.5-flash", "gemini-flash-latest", "gemini-2.0-flash-001", "gemini-1.5-flash-8b"]

for model_id in models_to_test:
    print(f"\n--- Probando {model_id} ---")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Hola, responde con solo la palabra EXITO"
        )
        print(f"RESULTADO {model_id}: {response.text}")
    except Exception as e:
        print(f"ERROR {model_id}: {e}")
