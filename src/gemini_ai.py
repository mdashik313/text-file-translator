import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def translate(text, target_language):
    PROMPT = f"Translate the given text to {target_language}(give main result only): \"{text}\""
    response = model.generate_content(PROMPT)
    return response.text

