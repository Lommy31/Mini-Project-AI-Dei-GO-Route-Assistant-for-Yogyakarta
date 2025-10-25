# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json, os
from collections import deque
from backend.chatbot import get_response  # harus sesuai lokasi file

app = Flask(__name__)
CORS(app)

# === load graph (dipakai oleh route map jika perlu) ===
data_path = os.path.join(os.path.dirname(__file__), "data", "graph_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    edges = json.load(f)

graph = {}
for a, b, dist in edges:
    graph.setdefault(a, []).append((b, dist))
    graph.setdefault(b, []).append((a, dist))

def shortest_route(start, end):
    from collections import deque
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

@app.route("/api/route", methods=["POST"])
def get_route():
    data = request.get_json() or {}
    start = data.get("start")
    end = data.get("end")
    result = shortest_route(start, end)
    if not result:
        return jsonify({"error": "Rute belum tersedia"}), 404
    path, distance = result
    return jsonify({"route": path, "distance": distance})

# === CHATBOT endpoint — gunakan get_response dari backend/chatbot.py ===
@app.route("/api/chatbot", methods=["POST"])
def api_chatbot():
    data = request.get_json(silent=True) or {}
    # terima baik 'message' atau 'user_input' dari frontend
    user_message = data.get("message") or data.get("user_input") or ""
    user_message = (user_message or "").strip()
    if not user_message:
        return jsonify({"response": "Pesannya kosong nih 😅. Coba ketik 'Aku mau ke UGM dari Malioboro'."})

    # panggil fungsi utama chatbot
    try:
        bot_reply = get_response(user_message)
    except Exception as e:
        # jangan crash — kirim pesan kesalahan yang jelas agar bisa debug
        bot_reply = f"Ada error di server saat memproses pesan: {e}"

    return jsonify({"response": bot_reply})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
