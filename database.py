import sqlite3
import os

DB_NAME = "consultorio.db"

def init_db():
    """Inicializa la base de datos con el esquema multitenencia."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabla de Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            whatsapp_token TEXT NOT NULL,
            phone_number_id TEXT NOT NULL UNIQUE,
            verify_token TEXT NOT NULL,
            system_instruction TEXT,
            stripe_api_key TEXT,
            bank_name TEXT,
            clabe TEXT,
            beneficiary_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Manejar actualizaciones de esquema para tablas existentes
    cursor.execute("PRAGMA table_info(clients)")
    client_columns = [column[1] for column in cursor.fetchall()]
    
    new_cols = {
        "bank_name": "TEXT",
        "clabe": "TEXT",
        "beneficiary_name": "TEXT",
        "stripe_api_key": "TEXT" 
    }
    
    for col, type in new_cols.items():
        if col not in client_columns:
            print(f"🔧 Agregando columna '{col}' a la tabla 'clients'...")
            cursor.execute(f'ALTER TABLE clients ADD COLUMN {col} {type}')
    
    # Tabla de Base de Conocimientos (Extraído de PDFs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            content TEXT NOT NULL,
            source_file TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Asegurar que la tabla exista primero
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            cliente_telefono TEXT,
            paciente_nombre TEXT,
            fecha_hora TEXT,
            motivo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')

    # Ahora verificar y agregar client_id si es necesario (para migraciones futuras)
    cursor.execute("PRAGMA table_info(citas)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "client_id" not in columns:
        print("🔧 Agregando columna 'client_id' a la tabla 'citas'...")
        cursor.execute('ALTER TABLE citas ADD COLUMN client_id INTEGER REFERENCES clients(id)')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos multitenencia inicializada.")

def migrate_existing_data():
    """Migra los datos existentes al primer cliente creado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Verificar si ya existe el cliente default (Dr. Omar)
    cursor.execute("SELECT id FROM clients WHERE name = 'Dr. Omar'")
    client = cursor.fetchone()
    
    if not client:
        # Insertar cliente default si no existe (usando los tokens actuales de main.py como ejemplo)
        # Nota: Estos deberían moverse a variables de entorno o ser configurados por el usuario
        print("🚀 Creando cliente default: Dr. Omar")
        cursor.execute('''
            INSERT INTO clients (name, whatsapp_token, phone_number_id, verify_token, system_instruction)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            "Dr. Omar", 
            "EAAdBmqZAtjBwBQM5dRVOeoo8kBZBFyJbExqgN98FmZCWZAvZBzp5Y7AGk4sU5IbicO4ogDMiZCKmZBzvP4tyuUL6WFUr5elbUQclLy0lezpH8T5m6hN7U614r5pHNXMv6mwYGZCqmglc0xUAvFD34AXk1qNPXWZAaYIGnCJW8P0ak2aZAZCYLXD5c86GFQvLB3k1fDkmsgrzPcpUASsC2hzBoDaE9Y2a4x8TO7Dlk9iq8YqhvaZBZCZCHDTh3Xm6t8DMPj7RIAoOTNf8IclArmHgt2zIlSZAgZDZD",
            "910272332169945",
            "MI_TOKEN_SECRETO_123",
            "Eres asistente del Dr. Omar. Tu objetivo es agendar citas médicas."
        ))
        client_id = cursor.lastrowid
        
        # Actualizar citas huérfanas
        cursor.execute("UPDATE citas SET client_id = ? WHERE client_id IS NULL", (client_id,))
        print(f"✅ Citas migradas al cliente ID: {client_id}")
    
    conn.commit()
    conn.close()

def get_client_by_phone_id(phone_number_id):
    """Obtiene los datos de un cliente por su Phone Number ID."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE phone_number_id = ?", (phone_number_id,))
    client = cursor.fetchone()
    conn.close()
    return client

def get_client_knowledge(client_id):
    """Obtiene toda la base de conocimientos asociada a un cliente."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM knowledge_base WHERE client_id = ?", (client_id,))
    rows = cursor.fetchall()
    conn.close()
    return "\n".join([row[0] for row in rows])

def guardar_cita(client_id, nombre, fecha_hora, motivo, telefono):
    """Guarda una cita asociada a un cliente específico."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO citas (client_id, paciente_nombre, fecha_hora, motivo, cliente_telefono) VALUES (?, ?, ?, ?, ?)",
            (client_id, nombre, fecha_hora, motivo, telefono)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ ERROR GUARDAR CITA: {e}")
        return False

if __name__ == "__main__":
    init_db()
    migrate_existing_data()
