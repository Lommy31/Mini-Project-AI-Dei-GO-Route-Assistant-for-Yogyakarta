from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# === Load data rute dari file JSON ===
with open("data/graph_data.json", "r", encoding="utf-8") as f:
    routes_data = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/route", methods=["POST"])
def get_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    # cari rute dari file json
    route = routes_data.get(f"{start}-{end}") or routes_data.get(f"{end}-{start}")

    if not route:
        return jsonify({"error": "Rute belum tersedia"}), 404

    distance = len(route)
    return jsonify({"route": route, "distance": distance})

@app.route("/api/chatbot", methods=["POST"])
def chatbot_reply():
    data = request.get_json()
    user_input = data.get("user_input", "").lower()

    if "ugm" in user_input and "malioboro" in user_input:
        response = "Rute terbaik dari Malioboro ke UGM adalah lewat Jalan Margo Utomo dan Cik Ditiro. Sekitar 15 menit perjalanan 🚗."
    elif "tugu" in user_input:
        response = "Tugu Jogja berada di pusat kota, dekat Malioboro. Simbol penting Yogyakarta!"
    elif "keraton" in user_input:
        response = "Keraton Yogyakarta adalah istana resmi Sultan, pusat budaya dan sejarah 👑."
    elif "halo" in user_input or "hai" in user_input:
        response = "Halo juga! 👋 Aku Dei-GO, asisten rute untuk destinasi di Yogyakarta."
    else:
        response = "Maaf, aku belum paham pertanyaan itu 😅. Coba tanya tentang rute di Yogyakarta!"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
