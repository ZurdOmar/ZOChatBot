import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Probando llave: ...{key[-4:]}")

client = genai.Client(api_key=key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hola, responde con la palabra EXITO si puedes leer esto."
    )
    print(f"RESULTADO: {response.text}")
except Exception as e:
    print(f"FALLO: {str(e)}")
