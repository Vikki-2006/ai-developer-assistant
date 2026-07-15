from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit()

client = genai.Client(api_key=api_key)

print("API Key Loaded Successfully")
print("Available Models:\n")

try:
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("ERROR:", e)
