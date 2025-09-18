import google.generativeai as genai
from .config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-pro"  # or another available model

def get_response(prompt: str) -> str:
    """Basic call to Gemini. Returns assistant text reply."""
    if not GEMINI_API_KEY:
        return "Gemini API key not configured."
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        result = model.generate_content(prompt)
        return (result.text or "").strip()
    except Exception as e:
        return f"Error calling Gemini: {e}"

def detect_action_intent(text: str) -> dict:
    """
    Ask Gemini to classify intent in a compact form (optional),
    but we also run simple rule-based parsing in actions.py.
    Returns a dict like {"action": "open_app", "target": "whatsapp"} if confident.
    """

    # Lightweight prompt: ask for single-line JSON
    prompt = f"""You are an assistant that extracts simple desktop intents. Respond ONLY with a JSON object. Given the user text: \"{text}\"
Return fields: action (open_app/open_url/call/none), target (string), extra (optional). If no action, return action: none.
Example: {{ "action":"open_app", "target":"whatsapp" }}"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        r = model.generate_content(prompt)
        out = (r.text or "").strip()
        # try to parse JSON:
        import json
        try:
            return json.loads(out)
        except:
            return {"action": "none", "target": "", "raw": out}
    except Exception:
        return {"action": "none", "target": ""}
