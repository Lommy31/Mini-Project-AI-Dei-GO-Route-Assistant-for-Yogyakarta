// static/chatbot.js
const chatbotButton = document.getElementById("chatbot-button");
const chatbotContainer = document.getElementById("chatbot-container");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chatbot-messages");

// toggle
chatbotButton.addEventListener("click", (e) => {
  chatbotContainer.style.display = chatbotContainer.style.display === "flex" ? "none" : "flex";
});

// helper untuk append pesan
function appendMessage(who, text) {
  const div = document.createElement("div");
  div.className = who === "user" ? "user-msg" : "bot-msg";
  div.innerHTML = `<div class="bubble">${text.replace(/\n/g, "<br>")}</div>`;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage("user", `Kamu: ${message}`);
  userInput.value = "";
  try {
    const res = await fetch("/api/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });
    const data = await res.json();
    appendMessage("bot", `Dei-GO: ${data.response}`);
  } catch (err) {
    appendMessage("bot", "Dei-GO: Maaf, terjadi kesalahan koneksi ke server.");
    console.error(err);
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
