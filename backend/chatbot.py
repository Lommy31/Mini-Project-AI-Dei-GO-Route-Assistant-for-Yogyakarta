import networkx as nx
import re

# =======================
# 🔹 GRAPH DATA
# =======================
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
    ("Monjali", "Bandara", 8)
]

G = nx.Graph()
for src, dest, dist in edges:
    G.add_edge(src.lower(), dest.lower(), weight=dist)

aliases = {
    "ugm": "ugm",
    "kampus ugm": "ugm",
    "universitas gadjah mada": "ugm",
    "tugu": "tugu jogja",
    "tugu jogja": "tugu jogja",
    "monjali": "monjali",
    "malioboro": "malioboro",
    "stasiun tugu": "stasiun tugu",
    "keraton": "keraton",
    "alun alun kidul": "alun-alun kidul",
    "alun-alun kidul": "alun-alun kidul",
    "bandara": "bandara",
}


# =======================
# 🔹 Fungsi Shortest Path
# =======================
def find_shortest_path(start, end):
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")
        return {"route": path, "distance": distance}
    except nx.NodeNotFound:
        return {"error": f"⚠️ Saya tidak mengenali destinasi tersebut. Coba sebutkan dua lokasi."}
    except nx.NetworkXNoPath:
        return {"error": f"⚠️ Tidak ada rute antara {start.title()} dan {end.title()}."}


# =======================
# 🔹 Chatbot Utama
# =======================
def get_response(user_input):
    """Chatbot sederhana untuk sapaan + perhitungan rute."""
    user_input = user_input.lower().strip()

    if user_input == "" or user_input in ["hai", "halo", "hey"]:
        return "Halo! 👋 Aku asisten rute Jogja kamu. Coba ketik 'dari UGM ke Bandara' untuk cari jalur tercepat!"
    elif "terima kasih" in user_input:
        return "Sama-sama! Senang bisa membantu 😊"
    elif "apa kabar" in user_input:
        return "Aku baik-baik aja! Siap bantu kamu cari rute hari ini 😄"

    # 🧭 Tambahan: dukung kalimat seperti "aku mau ke UGM dari Malioboro"
    match = re.search(r"(?:dari\s+([\w\s\-]+)\s+ke\s+([\w\s\-]+))|(?:ke\s+([\w\s\-]+)\s+dari\s+([\w\s\-]+))", user_input)
    if match:
        # Deteksi apakah formatnya “dari A ke B” atau “ke B dari A”
        if match.group(1) and match.group(2):
            start_raw = match.group(1).strip()
            end_raw = match.group(2).strip()
        else:
            start_raw = match.group(4).strip()
            end_raw = match.group(3).strip()

        start = aliases.get(start_raw.lower(), start_raw.lower())
        end = aliases.get(end_raw.lower(), end_raw.lower())

        result = find_shortest_path(start, end)
        if "error" in result:
            return result["error"]

        route = " → ".join([loc.title() for loc in result["route"]])
        return f"🚗 Rute tercepat dari {start_raw.title()} ke {end_raw.title()} adalah:\n{route}\n🛣️ Jarak total: {result['distance']} km"

    return "Maaf, aku belum paham maksudmu 😅. Coba ketik 'dari UGM ke Bandara' untuk contoh perhitungan rute!"
