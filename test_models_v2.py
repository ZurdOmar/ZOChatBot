from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-flash-latest"]

for model_id in models_to_test:
    print(f"\n--- Testing {model_id} ---")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="Dime hola y una lista de 5 servicios de IA brevemente."
        )
        print(f"✅ SUCCESS: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
