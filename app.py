import threading
import uvicorn
from fastapi import FastAPI
import streamlit as st
import requests

# === FastAPI bagian backend ===
app = FastAPI()

@app.post("/chatbot")
def chatbot(data: dict):
    user_input = data.get("user_input", "")
    # contoh respons sederhana (tanpa OpenAI)
    return {"response": f"Rute ke {user_input} sedang diproses oleh sistem AI sederhana 🚗"}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# === Jalankan FastAPI di thread terpisah ===
thread = threading.Thread(target=run_fastapi, daemon=True)
thread.start()

# === Streamlit bagian frontend ===
st.title("🗺️ Route Assistant Chatbot - Yogyakarta")

user_input = st.text_input("Ketik tujuanmu (contoh: Saya mau ke UGM dari Malioboro):")

if user_input:
    response = requests.post("https://mini-project-ai-dei-go-route-assistant-for-yogya-production.up.railway.app/api/chatbot", ...)
    st.write(response.json().get("response"))
