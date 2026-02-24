import os
import uvicorn
from fastapi import FastAPI, Request
from collections import deque
from dotenv import load_dotenv

# Módulos Propios
import database
import whatsapp_service
from gemini_service import GeminiEngine

# Cargar configuración
load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()

# Inicializar DB y Motor IA
database.init_db()
gemini = GeminiEngine(api_key=GEMINI_API_KEY)

@app.get("/webhook")
async def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    if token == VERIFY_TOKEN:
        challenge = request.query_params.get("hub.challenge")
        return int(challenge) if challenge else "Ok"
    return "Error auth", 403

# Caché para evitar procesar reintentos de WhatsApp (últimos 100 IDs)
PROCESSED_MESSAGES = deque(maxlen=100)

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    try:
        data = await request.json()
        
        # 1. Extraer datos básicos del mensaje
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        
        if 'messages' in value:
            message = value['messages'][0]
            message_id = message.get('id')
            
            # Si ya procesamos este mensaje, ignorarlo
            if message_id in PROCESSED_MESSAGES:
                print(f"⏭️ Mensaje duplicado ignorado: {message_id}")
                return {"status": "already_processed"}
            
            # Registrarlo de inmediato
            PROCESSED_MESSAGES.append(message_id)

            numero_usuario = message['from']
            texto_usuario = message.get('text', {}).get('body', "")
            phone_number_id = value['metadata']['phone_number_id']
            
            # Corrección para números de México
            if numero_usuario.startswith("521"):
                numero_usuario = numero_usuario.replace("521", "52", 1)
            
            print(f"📩 Mensaje de {numero_usuario} para el negocio {phone_number_id}: {texto_usuario}")
            with open("webhook_log.txt", "a", encoding="utf-8") as f:
                f.write(f"RECIBIDO: {numero_usuario} -> {texto_usuario} (ID: {phone_number_id})\n")
            
            # 2. Buscar al CLIENTE (Emprendimiento) en nuestra DB
            client_data = database.get_client_by_phone_id(phone_number_id)
            
            if not client_data:
                print(f"⚠️ Negocio no registrado: {phone_number_id}")
                with open("webhook_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"ERROR: Negocio no registrado {phone_number_id}\n")
                return {"status": "unrecognized_client"}

            # 3. Procesar con Gemini (RAG + Contexto del Cliente)
            respuesta_ai = gemini.generar_respuesta(texto_usuario, client_data, numero_usuario)
            print(f"🧠 Respuesta IA: {respuesta_ai[:50]}...")
            with open("webhook_log.txt", "a", encoding="utf-8") as f:
                f.write(f"GEMINI: {respuesta_ai[:50]}\n")
            
            # 4. Enviar respuesta por WhatsApp
            enviado = whatsapp_service.enviar_mensaje_whatsapp(
                numero=numero_usuario,
                texto=respuesta_ai,
                whatsapp_token=client_data['whatsapp_token'],
                phone_number_id=client_data['phone_number_id']
            )
            with open("webhook_log.txt", "a", encoding="utf-8") as f:
                f.write(f"ENVIADO: {enviado}\n")
            
    except Exception as e:
        print(f"🔥 Error en Webhook: {e}")
        with open("webhook_log.txt", "a", encoding="utf-8") as f:
            f.write(f"EXCEPCIÓN: {str(e)}\n")

    return {"status": "ok"}

if __name__ == "__main__":
    # Asegurar que el servidor corra en el puerto correcto
    uvicorn.run(app, host="0.0.0.0", port=8000)