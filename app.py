from flask import Flask, render_template, request, jsonify
import json, os
from collections import deque

app = Flask(__name__)

# --- Load graph data ---
data_path = os.path.join(os.path.dirname(__file__), "data", "graph_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    edges = json.load(f)

# Buat graph adjacency list
graph = {}
for a, b, dist in edges:
    graph.setdefault(a, []).append((b, dist))
    graph.setdefault(b, []).append((a, dist))  # graph dua arah


# --- Cari rute terpendek (BFS) ---
def shortest_route(start, end):
    if start not in graph or end not in graph:
        return None

    queue = deque([(start, [start], 0)])  # (node, path, total_distance)
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


# --- API ROUTE ---
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


# --- Chatbot sederhana ---
@app.route("/api/chatbot", methods=["POST"])
def chatbot_reply():
    data = request.get_json()
    user_input = data.get("user_input", "").lower()

    if "rute" in user_input or "ke" in user_input:
        return jsonify({
            "response": "Silakan gunakan fitur 'Select Your Route' di atas untuk mencari rute terbaik di Yogyakarta 🚗"
        })

    if "halo" in user_input or "hai" in user_input:
        response = "Halo juga! 👋 Aku Dei-GO, asisten rute Yogyakarta."
    elif "tugu" in user_input:
        response = "Tugu Jogja berada di pusat kota, dekat Malioboro. Simbol penting Yogyakarta!"
    elif "keraton" in user_input:
        response = "Keraton Yogyakarta adalah istana resmi Sultan, pusat budaya dan sejarah 👑."
    else:
        response = "Maaf, aku belum paham pertanyaan itu 😅. Coba tanya tentang rute di Yogyakarta!"

    return jsonify({"response": response})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
