import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY tidak ditemukan di Environment Variables!")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "message": "Server Ibarat AI Siap!"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not API_KEY:
            return jsonify({"reply": "Konfigurasi Server Salah: API Key tidak ditemukan."}), 500

        data = request.json
        if not data or 'message' not in data:
            return jsonify({"reply": "Pesan tidak boleh kosong."}), 400
        
        user_message = data.get('message')

        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Role: Kamu adalah asisten AI toko 'Ibarat Fragrance'.
        Tugas: Membantu pelanggan memilih parfum, menjelaskan aroma, dan ramah.
        Aturan: Jawab singkat, elegan, gunakan Bahasa Indonesia.
        
        User: {user_message}
        AI:"""

        response = model.generate_content(prompt)

        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI tidak memberikan respon. Coba ulangi pertanyaan Anda."})

    except Exception as e:
        print("--- ERROR START ---")
        print(traceback.format_exc())
        print("--- ERROR END ---")
        
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            return jsonify({"reply": "Gagal: API Key yang kamu masukkan di Koyeb salah."}), 500
        
        return jsonify({"reply": f"Terjadi kendala teknis. Coba sesaat lagi."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
