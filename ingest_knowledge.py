import sys
import sqlite3
import database
import pdf_processor

def ingest(client_id, pdf_path):
    """Extrae texto del PDF y lo guarda en la base de datos del cliente."""
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()
    
    try:
        success = pdf_processor.procesar_y_guardar_conocimiento(client_id, pdf_path, cursor)
        if success:
            conn.commit()
            print(f"✅ Conocimiento cargado exitosamente para el cliente ID: {client_id}")
        else:
            print("❌ No se pudo extraer texto del PDF.")
    except Exception as e:
        print(f"🔥 Error durante la ingesta: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python ingest_knowledge.py <client_id> <pdf_path>")
    else:
        cid = int(sys.argv[1])
        path = sys.argv[2]
        ingest(cid, path)
