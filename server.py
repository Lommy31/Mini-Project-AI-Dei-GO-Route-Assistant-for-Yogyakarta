from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import networkx as nx
import re
import os

app = Flask(__name__)
CORS(app)

# === Graph setup ===
edges = [
    ("Tugu Jogja", "Stasiun Tugu", 1),
    ("Tugu Jogja", "UGM", 4),
    ("Tugu Jogja", "Malioboro", 2),
    ("Stasiun Tugu", "Malioboro", 1),
    ("Malioboro", "Keraton", 2),
    ("Keraton", "Alun-Alun Kidul", 1),
    ("UGM", "Monjali", 3),
    ("UGM", "Bandara", 7),
]
G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src, dest, weight=dist)

# === Routes ===
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/route", methods=["POST"])
def route():
    data = request.get_json()
    start, end = data["start"], data["end"]
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")
        return jsonify({"route": path, "distance": distance})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# === Chatbot smart response ===
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input", "").lower()

    # Pola untuk deteksi rute: contoh "rute dari UGM ke Malioboro"
    pattern = r"rute dari (.+) ke (.+)"
    match = re.search(pattern, user_input)

    if match:
        start, end = match.group(1).strip().title(), match.group(2).strip().title()
        if start in G and end in G:
            try:
                path = nx.dijkstra_path(G, start, end, weight="weight")
                distance = nx.dijkstra_path_length(G, start, end, weight="weight")
                return jsonify({
                    "response": f"Berikut rute terbaik dari {start} ke {end}: {' → '.join(path)} (jarak {distance} km)"
                })
            except Exception:
                return jsonify({"response": f"Maaf, tidak ditemukan rute dari {start} ke {end}."})
        else:
            return jsonify({"response": "Pastikan nama tempatnya sesuai data yang ada ya!"})

    # Respon umum chatbot
    elif "halo" in user_input or "hai" in user_input:
        return jsonify({"response": "Halo! 👋 Mau cari rute ke mana hari ini?"})
    elif "terima kasih" in user_input:
        return jsonify({"response": "Sama-sama! Senang bisa bantu 😊"})
    elif "tempat" in user_input:
        places = ", ".join(sorted(G.nodes()))
        return jsonify({"response": f"Tempat yang tersedia: {places}"})
    else:
        return jsonify({"response": "Aku bisa bantu cariin rute, coba ketik: 'rute dari UGM ke Malioboro' 🚗"})

# === Run ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
