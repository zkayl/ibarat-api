from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

@app.route('/', methods=['GET'])
def home():
    return "Server AI Ibarat Fragrance Berjalan!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        system_instruction = """
        Kamu adalah asisten AI untuk toko 'Ibarat Fragrance'. 
        Tugasmu adalah merekomendasikan parfum berdasarkan suasana hati, aktivitas, atau preferensi aroma.
        Jawablah dengan ramah, singkat, dan elegan.
        Jika ditanya harga atau stok, arahkan user untuk melihat katalog atau hubungi WhatsApp.
        """
        
        full_prompt = f"{system_instruction}\n\nUser: {user_message}\nAI:"
        
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
    
    except Exception as e:
        return jsonify({"reply": f"Error Backend: {str(e)}"}), 500

if __name__ == '__main__':

    app.run(debug=True, port=8000)
