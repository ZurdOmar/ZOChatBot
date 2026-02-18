import sqlite3

def update_token():
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # NUEVO TOKEN proporcionado por el usuario
    new_token = 'EAAdBmqZAtjBwBQpjzVSOy9ZCXlxdHDw56ZATzxuEhS5OufIANSsBoMio7jPdt0FezCPX1FTM9mL2c1UNIWRYizPIcfuQwhXx5eTZASYRNK6DGmWdWJqU82clgTV9ShkjHyocb0XyP4TXib8Typrhy5LAT3g8pAVLbdK0ydZA4vzzljlN93WMmCEqBrZCav7wElZBpmPkcnubgTybuQ4bfAYGZCfdgWQE76Dn9p61WzrzkeoyGB1ANOBgkWXHLH1t4JBNo06rWyUSUiNyar361vjTEywZD'
    
    # Actualizar para el cliente ID 1 (que es el que estamos usando para Zotek ahora)
    query = "UPDATE clients SET whatsapp_token = ? WHERE id = 1"
    cursor.execute(query, (new_token.strip(),))
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT name, substr(whatsapp_token, 1, 20) FROM clients WHERE id = 1")
    updated = cursor.fetchone()
    print(f"✅ Token actualizado para {updated[0]}. Prefijo: {updated[1]}...")
    
    conn.close()

if __name__ == "__main__":
    update_token()
