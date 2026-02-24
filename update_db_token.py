import sqlite3
import sys

def update_token(phone_id, new_token):
    db_name = "consultorio.db"
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT id, name FROM clients WHERE phone_number_id = ?", (phone_id,))
        client = cursor.fetchone()
        
        if client:
            print(f"Found client: {client[1]} (ID: {client[0]})")
            cursor.execute("UPDATE clients SET whatsapp_token = ? WHERE phone_number_id = ?", (new_token, phone_id))
            conn.commit()
            print("✅ WhatsApp Token updated successfully in database.")
        else:
            print(f"❌ Error: No client found with Phone Number ID: {phone_id}")
            
        conn.close()
    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 update_db_token.py <PHONE_NUMBER_ID> <NEW_TOKEN>")
    else:
        update_token(sys.argv[1], sys.argv[2])
