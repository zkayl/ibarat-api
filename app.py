from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
import traceback

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable Koyeb
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inisialisasi Client Baru (Google Gen AI SDK)
client = genai.Client(api_key=GENAI_API_KEY)

@app.route('/', methods=['GET'])
def home():
    return "Server AI Ibarat Fragrance Berjalan dengan SDK Terbaru!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not GENAI_API_KEY:
            return jsonify({"reply": "Error: API Key Gemini belum dipasang di Koyeb!"}), 500

        data = request.json
        user_message = data.get('message')
        
        system_instruction = "Kamu adalah asisten AI toko Ibarat Fragrance. Jawablah dengan ramah, singkat, dan elegan."
        
        # Panggilan API versi SDK Baru
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{system_instruction}\n\nUser: {user_message}"
        )
        
        if not response.text:
            return jsonify({"reply": "Maaf, AI tidak memberikan respon."})

        return jsonify({"reply": response.text})
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details) 
        return jsonify({"reply": f"Terjadi Error di Backend: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
