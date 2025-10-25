const chatbotButton = document.getElementById("chatbot-button");
const chatbotContainer = document.getElementById("chatbot-container");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chatbot-messages");

// Toggle chatbot window
chatbotButton.addEventListener("click", () => {
  chatbotContainer.classList.toggle("hidden");
});

// Kirim pesan ke backend Flask
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // tampilkan pesan user
  chatMessages.innerHTML += `<div class="user"><b>Kamu:</b> ${message}</div>`;
  userInput.value = "";

  // kirim ke backend
  const res = await fetch("/api/chatbot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: message }),
  });

  const data = await res.json();
  chatMessages.innerHTML += `<div class="bot"><b>Dei-GO:</b> ${data.response}</div>`;

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Klik kirim
sendBtn.addEventListener("click", sendMessage);

// Tekan Enter
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
