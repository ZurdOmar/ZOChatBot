from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

models_to_test = [
    "gemini-2.0-flash-lite",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b"
]

for model_id in models_to_test:
    print(f"Testing {model_id}...")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents="hi"
        )
        print(f"✅ Success with {model_id}!")
        break
    except Exception as e:
        print(f"❌ Failed {model_id}: {e}")
        time.sleep(1)
