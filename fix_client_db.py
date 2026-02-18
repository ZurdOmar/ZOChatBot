import sqlite3

def fix_db():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # NUEVO TOKEN proporcionado por el usuario
    whatsapp_token = 'EAAdBmqZAtjBwBQpPPZCeKRq2OSPAosOcilZB1nG6cxEnSReWMJEQ2oJOPVQD5vpeeEaVUBZBCEmVZBRhq8Je7yKwNp9FZAS3uaYKbx5yiJUCgEO779eMweRksbFLdqkI11uQHg7Pn3eyeW7VCRs24xCxcA1pThMieM3sgIfir4b2Tydk8YjT3OHr8q78GuY36hZBYhQCDMVKwgziwZCGbjFq9X3UUTolfOZC0xgzMAKaEzaXhq0sPcI7E064UVrI5ZAHVIZBQGs3L6Y91FmnHHZARSCFUBgZD'
    phone_number_id = '910272332169945'
    
    query = """
    UPDATE clients 
    SET whatsapp_token = ?,
        phone_number_id = ?
    WHERE id = 1
    """
    
    cursor.execute(query, (whatsapp_token.strip(), phone_number_id))
    conn.commit()
    print("✅ Base de datos actualizada con el TOKEN de 24h correcto.")
    conn.close()

if __name__ == "__main__":
    fix_db()
