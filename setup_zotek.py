import sqlite3

def add_zotek_client():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # Datos de Zotek Soluciones IA
    name = 'Zotek Soluciones IA'
    whatsapp_token = 'EAAdBmqZAtjBwBQpPPZCeKRq2OSPAosOcilZB1nG6cxEnSReWMJEQ2oJOPVQD5vpeeEaVUBZBCEmVZBRhq8Je7yKwNp9FZAS3uaYKbx5yiJUCgEO779eMweRksbFLdqkI11uQHg7Pn3eyeW7VCRs24xCxcA1pThMieM3sgIfir4b2Tydk8YjT3OHr8q78GuY36hZBYhQCDMVKwgziwZCGbjFq9X3UUTolfOZC0xgzMAKaEzaXhq0sPcI7E064UVrI5ZAHVIZBQGs3L6Y91FmnHHZARSCFUBgZD'
    phone_number_id = '910272332169945' # ADVERTENCIA: Usamos el mismo ID de prueba, pero en producción cada uno tendría el suyo
    verify_token = 'MI_TOKEN_SECRETO_123'
    system_instruction = 'Eres un asesor experto de Zotek Soluciones IA. Ofreces servicios de automatización, chatbots e inteligencia artificial para empresas.'
    bank_name = 'SANTANDER'
    clabe = '012345678901234567'
    beneficiary_name = 'Zotek Soluciones IA'

    # Verificar si ya existe un cliente con ese phone_number_id
    cursor.execute("SELECT id FROM clients WHERE phone_number_id = ?", (phone_number_id,))
    existing = cursor.fetchone()
    
    if existing:
        print(f"⚠️ Ya existe un cliente con ID {phone_number_id}. Actualizando datos de Zotek en el registro existente (ID {existing[0]}).")
        query = """
        UPDATE clients 
        SET name = ?, whatsapp_token = ?, verify_token = ?, system_instruction = ?, bank_name = ?, clabe = ?, beneficiary_name = ?
        WHERE id = ?
        """
        cursor.execute(query, (name, whatsapp_token, verify_token, system_instruction, bank_name, clabe, beneficiary_name, existing[0]))
    else:
        query = """
        INSERT INTO clients (name, whatsapp_token, phone_number_id, verify_token, system_instruction, bank_name, clabe, beneficiary_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (name, whatsapp_token, phone_number_id, verify_token, system_instruction, bank_name, clabe, beneficiary_name))
    
    conn.commit()
    print("✅ Cliente 'Zotek Soluciones IA' registrado exitosamente.")
    conn.close()

if __name__ == "__main__":
    add_zotek_client()
