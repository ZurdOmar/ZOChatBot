import sqlite3

def stabilize_bot():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # 1. Simplificar instrucción maestra
    new_instruction = "Eres un experto de Zotek Soluciones IA. Proporciona información sobre nuestros servicios de forma clara y profesional."
    cursor.execute("UPDATE clients SET system_instruction = ? WHERE id = 1", (new_instruction,))
    
    # 2. Limpiar y truncar conocimiento (máximo 1500 caracteres para estabilidad)
    cursor.execute("SELECT content FROM knowledge_base WHERE client_id = 1")
    rows = cursor.fetchall()
    full_content = "\n".join([r[0] for r in rows if r[0]])
    
    # Limpiar un poco el texto si tiene caracteres extraños
    cleaned_content = full_content.replace('\x00', '') # Por si acaso
    truncated = cleaned_content[:1500] 
    
    cursor.execute("DELETE FROM knowledge_base WHERE client_id = 1")
    cursor.execute("INSERT INTO knowledge_base (client_id, content) VALUES (1, ?)", (truncated,))
    
    conn.commit()
    print(f"✅ Bot estabilizado.")
    print(f"   - Instrucción: {new_instruction}")
    print(f"   - Conocimiento (cars): {len(truncated)}")
    conn.close()

if __name__ == "__main__":
    stabilize_bot()
