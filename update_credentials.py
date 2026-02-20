import sqlite3
import sys

def update_credentials(new_token, new_phone_id):
    try:
        conn = sqlite3.connect('consultorio.db')
        cursor = conn.cursor()
        
        # We assume client ID 1 is Zotek Soluciones IA based on previous plan
        query = "UPDATE clients SET whatsapp_token = ?, phone_number_id = ? WHERE id = 1"
        cursor.execute(query, (new_token.strip(), new_phone_id.strip()))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Credenciales actualizadas exitosamente en consultorio.db para el cliente ID 1.")
        else:
            print(f"⚠️ No se encontró el cliente con ID 1 en la base de datos.")
            
        conn.close()
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python update_credentials.py <token> <phone_id>")
    else:
        update_credentials(sys.argv[1], sys.argv[2])
