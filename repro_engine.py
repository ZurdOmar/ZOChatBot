import os
from dotenv import load_dotenv
from gemini_service import GeminiEngine

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Datos exactos que recibe el bot
client_data = {
    'id': 1,
    'name': 'Dr. Omar',
    'system_instruction': 'Eres un asistente médico para agendar citas médicas.',
    'clabe': '123456789012345678',
    'bank_name': 'SANTANDER',
    'beneficiary_name': 'Omar Morentin Lopez',
    'stripe_api_key': None
}
numero_usuario = '523123173431'
texto_usuario = 'hola'

engine = GeminiEngine(api_key=api_key)
print(f"Probando respuesta con modelo: {engine.model_id}")

respuesta = engine.generar_respuesta(texto_usuario, client_data, numero_usuario)
print(f"RESULTADO: {respuesta}")

# Verificar si se creó el log de error
if os.path.exists("gemini_error.log"):
    with open("gemini_error.log", "r") as f:
        print("\n--- ÚLTIMO ERROR REGISTRADO ---")
        print(f.readlines()[-10:])
