from flask import Flask, render_template, request, jsonify
import networkx as nx

app = Flask(__name__)

# === ROUTE LOGIC ===
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
