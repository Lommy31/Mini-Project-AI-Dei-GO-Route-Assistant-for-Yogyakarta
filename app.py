from flask import Flask, render_template, request, jsonify
import json, os
from collections import deque
from backend.chatbot import get_response

app = Flask(__name__)

# ================================
# 🔹 LOAD DATA GRAPH
# ================================
data_path = os.path.join(os.path.dirname(__file__), "data", "graph_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    edges = json.load(f)

# Buat graph adjacency list
graph = {}
for a, b, dist in edges:
    graph.setdefault(a, []).append((b, dist))
    graph.setdefault(b, []).append((a, dist))


# ================================
# 🔹 CARI RUTE TERPENDEK (BFS)
# ================================
def shortest_route(start, end):
    if start not in graph or end not in graph:
        return None

    queue = deque([(start, [start], 0)])  # node, path, distance
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


# ================================
# 🔹 API UNTUK RUTE (MAP)
# ================================
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


# ================================
# 🔹 CHATBOT (PAKAI backend/chatbot.py)
# ================================
@app.route("/api/chatbot", methods=["POST"])
def chat():
    data = request.get_json()

    # validasi input
    if not data or "message" not in data or not data["message"].strip():
        return jsonify({
            "response": "Pesannya kosong nih 😅. Coba ketik 'Aku mau ke UGM dari Malioboro'."
        })

    user_message = data["message"]
    bot_reply = get_response(user_message)  # 🧠 panggil fungsi dari chatbot.py
    return jsonify({"response": bot_reply})


# ================================
# 🔹 HALAMAN UTAMA
# ================================
@app.route("/")
def index():
    return render_template("index.html")


# ================================
# 🔹 RUN SERVER
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
