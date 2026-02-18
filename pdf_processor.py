from pypdf import PdfReader
import os

def extraer_texto_pdf(file_path):
    """Extrae el texto de un archivo PDF."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ ERROR PDF [{file_path}]: {e}")
        return None

def procesar_y_guardar_conocimiento(client_id, pdf_path, cursor):
    """Extrae texto de un PDF y lo guarda en la base de datos para un cliente."""
    print(f"📂 Procesando PDF: {pdf_path} para cliente {client_id}")
    texto = extraer_texto_pdf(pdf_path)
    if texto:
        cursor.execute('''
            INSERT INTO knowledge_base (client_id, content, source_file)
            VALUES (?, ?, ?)
        ''', (client_id, texto, os.path.basename(pdf_path)))
        return True
    return False
