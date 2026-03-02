# test_gemini_simple.py
import google.generativeai as genai

# Replace with your actual API key
API_KEY = "AIzaSyBo7H8Ne6nlunmG6RCuNeeLDE1tyTk89sc"   # ← your key here

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')   # or 'gemini-1.5-pro', 'gemini-2.0-flash-exp', etc.

    response = model.generate_content("Say hello in one sentence and tell me today's date.")
    
    print("SUCCESS! Gemini API is working.")
    print("\nResponse:")
    print(response.text.strip())

except Exception as e:
    print("FAILED to connect to Gemini API")
    print("Error:", str(e))