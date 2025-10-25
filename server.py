from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import networkx as nx
import re
import os

app = Flask(__name__)
CORS(app)

# === GRAPH SETUP ===
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


# === ROUTE API ===
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


# === CHATBOT (SMART VERSION) ===
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_input = data.get("user_input", "").lower().strip()

    # Pola deteksi rute, contoh: "rute dari ugm ke malioboro"
    pattern = r"rute dari (.+) ke (.+)"
