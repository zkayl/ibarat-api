from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import traceback

app = Flask(__name__)
CORS(app)

GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Server AI Ibarat Fragrance Berjalan!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not GENAI_API_KEY:
            return jsonify({"reply": "Error: API Key Gemini belum dipasang di Environment Variables Koyeb!"}), 500

        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        data = request.json
        user_message = data.get('message')
        
        system_instruction = "Kamu adalah asisten AI toko Ibarat Fragrance. Jawablah dengan ramah dan singkat."
        full_prompt = f"{system_instruction}\n\nUser: {user_message}\nAI:"
        
        response = model.generate_content(full_prompt)
        
        if not response.text:
            return jsonify({"reply": "Maaf, pertanyaan kamu tidak bisa dijawab oleh filter keamanan AI."})

        return jsonify({"reply": response.text})
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        return jsonify({"reply": f"Terjadi Error di Backend: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
