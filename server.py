from flask import Flask, request, jsonify
from flask_cors import CORS
import networkx as nx
from chatbot import get_response  # fungsi chatbot kamu

app = Flask(__name__)
CORS(app)  # biar frontend bisa akses tanpa diblok CORS

# =====================================================
# 🚏 GRAPH SETUP
# =====================================================
edges = [
    ("Tugu Jogja", "Stasiun Tugu", 1),
    ("Tugu Jogja", "UGM", 4),
    ("Tugu Jogja", "Malioboro", 2),
    ("Stasiun Tugu", "Malioboro", 1),
    ("Malioboro", "Keraton", 2),
    ("Malioboro", "UGM", 4),
    ("Keraton", "Alun-Alun Kidul", 1),
    ("Keraton", "UGM", 5),
    ("Alun-Alun Kidul", "Bandara", 9),
    ("UGM", "Monjali", 3),
    ("UGM", "Bandara", 7),
    ("Monjali", "Bandara", 8),
]

# Buat graf
G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src, dest, weight=dist)


# =====================================================
# 🧭 Shortest Path Function
# =====================================================
def find_shortest_path(start, end):
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")
        return path, distance
    except nx.NodeNotFound as e:
        return [], f"Node tidak ditemukan: {e}"
    except nx.NetworkXNoPath:
        return [], f"Tidak ada rute antara {start} dan {end}"


# =====================================================
# 💬 Chatbot Endpoint
# =====================================================
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = get_response(user_input)
    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"response": "Maaf, saya tidak mengerti."})


# =====================================================
# 🚗 Route Endpoint
# =====================================================
@app.route("/api/route", methods=["POST"])
def route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        return jsonify({"error": "Start dan end harus diisi"}), 400

    route, distance = find_shortest_path(start, end)
    if isinstance(distance, str):  # berarti error message
        return jsonify({"error": distance})

    return jsonify({"route": route, "distance": distance})


# =====================================================
# 🚀 Run Server
# =====================================================
if __name__ == "__main__":
    print("🚀 Running Flask server at http://127.0.0.1:5000 ...")
    app.run(debug=True)
