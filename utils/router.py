# utils/router.py
from models.local_model import query_local_model
from models.gemini_model import query_gemini

def choose_model(prompt):
    """
    Routes prompt to Local or Gemini model depending on complexity.
    Includes fallback if any model fails.
    """
    print(f"[Router] Received input: {prompt}")

    try:
        if len(prompt.split()) < 10:
            print("[Router] Using Local Model")
            response = query_local_model(prompt)
        else:
            print("[Router] Using Gemini Model")
            response = query_gemini(prompt)

        # Fallback if empty response
        if not response or response.strip() == "":
            print("[Router] Warning: Model returned empty response. Using fallback message.")
            response = "I'm still learning, but I understood your question!"

        print(f"[Router] Final Response: {response}")
        return response

    except Exception as e:
        print(f"[Router Error]: {e}")
        return "⚠️ AI model connection failed — using default fallback."
