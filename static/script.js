document.addEventListener("DOMContentLoaded", () => {
  const routeOutput = document.getElementById("route-output");
  const originSelect = document.getElementById("origin");
  const destinationSelect = document.getElementById("destination");
  const findRouteBtn = document.getElementById("find-route-btn");

  const chatOutput = document.getElementById("chatbox"); // <== ID-nya di HTML kamu chatbox, bukan chat-output
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  const locationImages = {
    "Tugu Jogja": "assets/images/tugu.jpg",
    Malioboro: "assets/images/malioboro.jpg",
    Keraton: "assets/images/keraton.jpg",
    "Stasiun Tugu": "assets/images/tugu.jpg",
    "Alun-Alun Kidul": "assets/images/keraton.jpg",
    UGM: "assets/images/tugu.jpg",
    Monjali: "assets/images/tugu.jpg",
    Bandara: "assets/images/tugu.jpg",
  };

  // =========================
  // FIND ROUTE BUTTON
  // =========================
  findRouteBtn.addEventListener("click", async () => {
    const origin = originSelect.value;
    const destination = destinationSelect.value;

    if (!origin || !destination) {
      routeOutput.innerHTML =
        "<p>Please select both origin and destination.</p>";
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start: origin, end: destination }),
      });

      if (!response.ok) throw new Error("Failed to fetch route data.");

      const data = await response.json();
      const route = data.route.join(" → ");
      const distance = data.distance;

      routeOutput.innerHTML = `
        <p><b>Route:</b> ${route}</p>
        <p><b>Distance:</b> ${distance} km</p>
        <div>
          <img src="${locationImages[origin]}" alt="${origin}">
          <img src="${locationImages[destination]}" alt="${destination}">
        </div>
      `;
    } catch (error) {
      routeOutput.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });

  // =========================
  // CHATBOT INTEGRATION
  // =========================
  sendBtn.addEventListener("click", async () => {
    const userMessage = userInput.value.trim();
    if (!userMessage) {
      addMessage("You", "Please enter a message.");
      return;
    }

    addMessage("You", userMessage);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to fetch chatbot response.");

      const data = await response.json();
      addMessage("Dei-GO", data.response || "Maaf, saya tidak mengerti.");
    } catch (error) {
      addMessage("Dei-GO", `Error: ${error.message}`);
    }

    userInput.value = "";
  });

  // =========================
  // CHAT MESSAGE HANDLER
  // =========================
  function addMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender === "You" ? "user-message" : "bot-message");
    messageDiv.innerHTML = `<div class="bubble">${message}</div>`;
    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  // =========================
  // ROUTE GRAPH VISUALIZATION
  // =========================
  const graphCanvas = document.getElementById("graphCanvas");
  const ctx = graphCanvas ? graphCanvas.getContext("2d") : null;

  function drawGraph() {
    if (!ctx) return;
    ctx.clearRect(0, 0, graphCanvas.width, graphCanvas.height);

    const nodes = {
      "Tugu Jogja": { x: 100, y: 100 },
      Malioboro: { x: 300, y: 100 },
      Keraton: { x: 500, y: 300 },
    };

    const edges = [
      ["Tugu Jogja", "Malioboro"],
      ["Malioboro", "Keraton"],
    ];

    ctx.strokeStyle = "#4f46e5";
    ctx.lineWidth = 2;
    edges.forEach(([from, to]) => {
      const fromNode = nodes[from];
      const toNode = nodes[to];
      ctx.beginPath();
      ctx.moveTo(fromNode.x, fromNode.y);
      ctx.lineTo(toNode.x, toNode.y);
      ctx.stroke();
    });

    Object.entries(nodes).forEach(([name, { x, y }]) => {
      ctx.fillStyle = "#4f46e5";
      ctx.beginPath();
      ctx.arc(x, y, 10, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#000";
      ctx.fillText(name, x - 30, y - 15);
    });
  }

  drawGraph();
});
