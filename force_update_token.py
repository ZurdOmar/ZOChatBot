import sqlite3

def force_update():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # Token exacto proporcionado por el usuario
    new_token = 'EAAdBmqZAtjBwBQpPPZCeKRq2OSPAosOcilZB1nG6cxEnSReWMJEQ2oJOPVQD5vpeeEaVUBZBCEmVZBRhq8Je7yKwNp9FZAS3uaYKbx5yiJUCgEO779eMweRksbFLdqkI11uQHg7Pn3eyeW7VCRs24xCxcA1pThMieM3sgIfir4b2Tydk8YjT3OHr8q78GuY36hZBYhQCDMVKwgziwZCGbjFq9X3UUTolfOZC0xgzMAKaEzaXhq0sPcI7E064UVrI5ZAHVIZBQGs3L6Y91FmnHHZARSCFUBgZD'
    
    cursor.execute("UPDATE clients SET whatsapp_token = ? WHERE id = 1", (new_token.strip(),))
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT whatsapp_token FROM clients WHERE id = 1")
    updated = cursor.fetchone()[0]
    print(f"VERIFICACIÓN: {updated[:20]}...")
    
    conn.close()

if __name__ == '__main__':
    force_update()
