# import google.generativeai as genai
# import os
# import dotenv
# dotenv.load_dotenv()


# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash-latest")

# async def translate(source_text, target_language):
#     PROMPT = f"Translate the given text to {target_language}(give translated text only): \"{source_text}\""
#     response = model.generate_content(PROMPT)
#     print("translation completed[from gemini api].")
#     return response.text


import os
import dotenv
dotenv.load_dotenv()
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def translate(source_text, target_language):
    PROMPT = f"Translate the given text to {target_language}(give translated text only): \"{source_text}\""
    response = client.models.generate_content(model="gemini-3-flash-latest", contents=PROMPT)
    print(response.text)
    print("translation completed[from gemini api].")
    return response.text

