from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import networkx as nx
import os
import json

app = Flask(__name__)
CORS(app)

# === Load graph data from JSON ===
with open(os.path.join("data", "graph_data.json"), "r") as f:
    edges = json.load(f)

# === Build graph ===
G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src, dest, weight=dist)

# === ROUTES ===
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

# === NEW: Send list of all locations ===
@app.route("/api/locations")
def get_locations():
    return jsonify(sorted(G.nodes()))

# === Chatbot (simple example) ===
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input", "")
    return jsonify({"response": f"Rute ke {user_input} sedang diproses 🚗"})

# === Run ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
