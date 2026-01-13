import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# This will print every model your key can actually see
print("--- AVAILABLE MODELS ---")
for model in client.models.list():
    print(f"Name: {model.name} | Supported Actions: {model.supported_generation_methods}")