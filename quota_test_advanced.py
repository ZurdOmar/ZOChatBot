from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def test_tool(a: str):
    """Test tool."""
    return f"Hello {a}"

model_id = "gemini-flash-latest"
print(f"Testing {model_id} with tools and system instruction...")

try:
    response = client.models.generate_content(
        model=model_id,
        config={
            "system_instruction": "You are a helpful assistant.",
            "tools": [test_tool],
        },
        contents="Hola"
    )
    print(f"✅ Success! Response: {response.text or 'Function Call detected'}")
except Exception as e:
    print(f"❌ Failed: {e}")
