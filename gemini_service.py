from google import genai
from google.genai import types
import os
import database
import time
import traceback

class GeminiEngine:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-flash-latest"

    def generar_respuesta(self, mensaje_usuario, client_data, numero_telefono):
        """Genera una respuesta inteligente basada en el contexto del cliente y su base de conocimientos."""
        
        client_id = client_data['id']
        nombre_cliente = client_data['name']
        
        # 1. Recuperar conocimiento específico del PDF/DB
        conocimiento = database.get_client_knowledge(client_id)
        
        # 2. Configurar la instrucción maestra con el contexto dinámico
        prompt_sistema = f"""
        Eres un experto de Zotek Soluciones IA. Proporciona información sobre nuestros servicios de forma clara y profesional.
        Sé amable, breve y usa el siguiente conocimiento para responder.
        
        CONOCIMIENTO:
        {conocimiento}
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    config={
                        "system_instruction": prompt_sistema,
                        "temperature": 0.5,
                    },
                    contents=mensaje_usuario
                )
                return response.text

            except Exception as e:
                error_str = str(e)
                # Si es un error de cuota o de servidor, reintentamos con backoff
                if ("503" in error_str or "429" in error_str) and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"⚠️ Reintentando Gemini ({attempt+1}/{max_retries}) en {wait_time}s por error: {error_str[:50]}...")
                    time.sleep(wait_time)
                    continue
                
                # Para errores permanentes o si se acabaron los reintentos
                error_msg = f"💀 ERROR GEMINI ({type(e).__name__}): {error_str}\n{traceback.format_exc()}"
                print(error_msg)
                with open("gemini_error.log", "a", encoding="utf-8") as f:
                    f.write(error_msg + "\n" + "="*50 + "\n")
                return "Lo siento, tuve un problema procesando tu mensaje. ¿Puedes repetirlo?"

        return "Lo siento, tuve un problema procesando tu mensaje. ¿Puedes repetirlo?"
