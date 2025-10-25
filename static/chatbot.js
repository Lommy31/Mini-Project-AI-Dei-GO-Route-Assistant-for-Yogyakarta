const chatbotButton = document.getElementById("chatbot-button");
const chatbotContainer = document.getElementById("chatbot-container");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chatbot-messages");

// === ANIMATED POP EFFECT ===
function showPopBubble(x, y) {
  const bubble = document.createElement("div");
  bubble.className = "chatbot-pop";
  bubble.textContent = "💬";
  bubble.style.left = `${x}px`;
  bubble.style.top = `${y}px`;
  document.body.appendChild(bubble);

  // animasi fade-out dan hapus elemen
  setTimeout(() => {
    bubble.style.opacity = "0";
    bubble.style.transform = "translateY(-30px) scale(0.8)";
  }, 50);

  setTimeout(() => {
    bubble.remove();
  }, 600);
}

// === TOGGLE CHATBOT WINDOW ===
chatbotButton.addEventListener("click", (e) => {
  // toggle tampil/sembunyi chatbot
  chatbotContainer.style.display =
    chatbotContainer.style.display === "flex" ? "none" : "flex";

  // munculkan efek bubble di posisi cursor
  showPopBubble(e.clientX, e.clientY);
});

// === CHATBOT CORE ===
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // tampilkan pesan user
  chatMessages.innerHTML += `<div class="user-msg"><b>Kamu:</b> ${message}</div>`;
  userInput.value = "";

  // kirim ke backend Flask
  const res = await fetch("/api/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: message }),
  });

  const data = await res.json();
  chatMessages.innerHTML += `<div class="bot-msg"><b>Dei-GO:</b> ${data.response}</div>`;
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Klik kirim
sendBtn.addEventListener("click", sendMessage);

// Tekan Enter
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
