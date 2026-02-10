import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable Koyeb
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY tidak ditemukan di Environment Variables!")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "message": "Server Ibarat AI Siap!"
    }), 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not API_KEY:
            return jsonify({
                "reply": "Konfigurasi server salah: API Key tidak ditemukan."
            }), 500

        data = request.get_json(silent=True)
        if not data or not data.get("message"):
            return jsonify({
                "reply": "Pesan tidak boleh kosong."
            }), 400

        user_message = data["message"]

        # ✅ MODEL RESMI & AMAN
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
Role: Kamu adalah asisten AI toko "Ibarat Fragrance".
Tugas: Membantu pelanggan memilih parfum, menjelaskan aroma, dan ramah.
Aturan:
- Jawaban singkat & elegan
- Bahasa Indonesia
- Nada profesional tapi hangat

User: {user_message}
AI:
"""

        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return jsonify({"reply": response.text.strip()})

        return jsonify({
            "reply": "AI belum bisa memberikan jawaban. Silakan coba lagi."
        }), 500

    except Exception:
        print("=== ERROR TRACEBACK ===")
        print(traceback.format_exc())

        return jsonify({
            "reply": "Terjadi kendala teknis di server. Silakan coba lagi."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

