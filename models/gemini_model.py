# models/gemini_model.py
import google.generativeai as genai

# Set your API key here
genai.configure(api_key="AIzaSyD75tvk1DVoVF7Vg_FQ58eDrRf3WGuk3XU")

def query_gemini(prompt):
    """
    Query Gemini model for complex tasks.
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini Error] {e}"
