import sqlite3

# 1. Conectamos al archivo de base de datos
conn = sqlite3.connect("consultorio.db")
cursor = conn.cursor()

# 2. Ejecutamos la consulta
print("\n" + "="*40)
print("📊 REPORTE DE CITAS (TABLA: citas)")
print("="*40)

try:
    cursor.execute("SELECT id, paciente_nombre, fecha_hora, motivo, cliente_telefono FROM citas")
    registros = cursor.fetchall()

    if not registros:
        print("📭 La tabla está vacía.")
    else:
        for cita in registros:
            print(f"🆔 ID: {cita[0]}")
            print(f"👤 Paciente: {cita[1]}")
            print(f"📅 Fecha: {cita[2]}")
            print(f"📝 Motivo: {cita[3]}")
            print(f"📱 Teléfono: {cita[4]}")
            print("-" * 20)

except Exception as e:
    print(f"❌ Error leyendo la base de datos: {e}")

conn.close()