import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Memperbolehkan semua origin agar tidak masalah saat diakses dari Netlify
CORS(app)

# Ambil API Key dari Environment Variable Koyeb
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
            return jsonify({"reply": "Konfigurasi Server Salah: API Key tidak ditemukan di Koyeb."}), 500

        # Ambil data dari request
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"reply": "Pesan tidak boleh kosong."}), 400
        
        user_message = data.get('message')

        # Inisialisasi Model (Gunakan 1.5-flash yang paling stabil di library ini)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Instruksi sistem
        prompt = f"""
        Role: Kamu adalah asisten AI toko 'Ibarat Fragrance'.
        Tugas: Membantu pelanggan memilih parfum, menjelaskan aroma, dan ramah.
        Aturan: Jawab singkat, elegan, gunakan Bahasa Indonesia.
        
        User: {user_message}
        AI:"""

        # Panggil AI
        response = model.generate_content(prompt)

        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "AI sedang tidak memberikan respon. Coba ulangi pertanyaan Anda."})

    except Exception as e:
        # Cetak error lengkap di Log Koyeb
        print("--- DEBUG ERROR ---")
        print(traceback.format_exc())
        
        error_msg = str(e)
        # Handle error 404 spesifik jika library gagal mapping model
        if "404" in error_msg:
            return jsonify({"reply": "Gagal: Model AI tidak ditemukan di region server ini. Cek API Key Anda."}), 500
        
        return jsonify({"reply": f"Terjadi kendala teknis di server. Silakan coba lagi."}), 500

if __name__ == '__main__':
    # Koyeb akan otomatis menggunakan gunicorn, port ini hanya untuk lokal
    app.run(host='0.0.0.0', port=8000)
