from flask import Flask, render_template, request, jsonify
import json, os
from collections import deque
from backend.chatbot import get_response

app = Flask(__name__)

# --- Load graph data ---
data_path = os.path.join(os.path.dirname(__file__), "data", "graph_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    edges = json.load(f)

# Buat graph adjacency list
graph = {}
for a, b, dist in edges:
    graph.setdefault(a, []).append((b, dist))
    graph.setdefault(b, []).append((a, dist))


# --- Cari rute terpendek (BFS) ---
def shortest_route(start, end):
    if start not in graph or end not in graph:
        return None
    queue = deque([(start, [start], 0)])
    visited = set()
    while queue:
        node, path, dist = queue.popleft()
        if node == end:
            return path, dist
        visited.add(node)
        for neighbor, d in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], dist + d))
    return None


# --- API untuk rute ---
@app.route("/api/route", methods=["POST"])
def get_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    result = shortest_route(start, end)
    if not result:
        return jsonify({"error": "Rute belum tersedia"}), 404
    path, distance = result
    return jsonify({"route": path, "distance": distance})


# --- Chatbot ---
@app.route("/api/chatbot", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").lower().strip()
    except Exception as e:
        return jsonify({"response": f"Format pesan tidak valid: {e}"}), 400

    if not user_message:
        return jsonify({"response": "Pesannya kosong nih 😅. Coba ketik 'Aku mau ke UGM dari Malioboro'."})

    # Kasus nanya rute
    if "ke" in user_message and "dari" in user_message:
        parts = user_message.split("dari")
        destination = parts[0].replace("aku mau ke", "").strip().title()
        origin = parts[1].strip().title()
        result = shortest_route(origin, destination)

        if result:
            path, distance = result
            route_str = " → ".join(path)
            return jsonify({
                "response": f"Rute tercepat dari {origin} ke {destination} adalah {route_str} dengan jarak sekitar {distance} km 🚗."
            })
        else:
            return jsonify({
                "response": f"Maaf, aku belum punya data rute dari {origin} ke {destination} 😢."
            })

    # Kasus sapaan umum
    if "halo" in user_message or "hai" in user_message:
        response = "Halo juga! 👋 Aku Dei-GO, asisten rute Yogyakarta."
    elif "tugu" in user_message:
        response = "Tugu Jogja berada di pusat kota, dekat Malioboro. Simbol penting Yogyakarta!"
    elif "keraton" in user_message:
        response = "Keraton Yogyakarta adalah istana resmi Sultan, pusat budaya dan sejarah 👑."
    else:
        response = "Coba ketik tujuanmu, misalnya: Aku mau ke UGM dari Malioboro 🗺️"

    return jsonify({"response": response})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
