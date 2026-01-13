import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- 🧠 K.O.D.A. AVAILABLE BRAINS ---")
try:
    # We fetch the list of models available to YOUR key
    for m in client.models.list():
        # In 2026, the attribute is 'supported_actions'
        if "generateContent" in m.supported_actions:
            print(f"✅ MODEL NAME: {m.name}")
            print(f"   (Display Name: {m.display_name})")
except Exception as e:
    print(f"❌ Diagnostic failed: {e}")