import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Testing API Key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say hello!")
    print("Gemini API call success!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Gemini API call failed: {e}")
