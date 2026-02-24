import sqlite3
import sys

def add_new_client(name, token, phone_id, verify_token, system_instr):
    try:
        conn = sqlite3.connect('consultorio.db')
        cursor = conn.cursor()
        
        query = """
        INSERT INTO clients (name, whatsapp_token, phone_number_id, verify_token, system_instruction)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (name, token, phone_id, verify_token, system_instr))
        client_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Cliente '{name}' registrado exitosamente con ID: {client_id}")
        print(f"📌 Ahora puedes cargar su conocimiento con: python3 ingest_knowledge.py {client_id} <path_to_pdf>")
        
        conn.close()
    except Exception as e:
        print(f"❌ Error al agregar cliente: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Uso: python3 add_client.py \"Nombre\" \"Token\" \"Phone_ID\" \"Verify_Token\" \"Instruccion_IA\"")
        print("Ejemplo: python3 add_client.py \"Dr. Garcia\" \"EAAdB...\" \"123456789\" \"TOKEN_SEC\" \"Eres el asistente del Dr. Garcia.\"")
    else:
        add_new_client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
