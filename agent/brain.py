from agent.config import USE_GEMINI, GEMINI_API_KEY

def get_response(prompt):
    if USE_GEMINI:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    else:
        return "No model selected"