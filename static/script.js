// ===============================
// DEI-GO Route Assistant
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  // =========================
  // ELEMENT REFERENCES
  // =========================
  const routeOutput = document.getElementById("route-output");
  const originSelect = document.getElementById("origin");
  const destinationSelect = document.getElementById("destination");
  const findRouteBtn = document.getElementById("find-route-btn");

  const chatOutput = document.getElementById("chatbox");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // =========================
  // LOCATION DATA
  // =========================
  const locationData = {
    "Tugu Jogja": {
      desc: "A historical landmark in the heart of Yogyakarta.",
      img: "assets/images/tugu.jpg",
      coords: [-7.7829, 110.3671],
    },
    Malioboro: {
      desc: "The most famous shopping street in Yogyakarta.",
      img: "assets/images/malioboro.jpg",
      coords: [-7.7930, 110.3658],
    },
    Keraton: {
      desc: "The magnificent Sultan’s Palace.",
      img: "assets/images/keraton.jpg",
      coords: [-7.8056, 110.3649],
    },
    "Alun-Alun Kidul": {
      desc: "A popular night attraction in Yogyakarta.",
      img: "assets/images/keraton.jpg",
      coords: [-7.8111, 110.3643],
    },
    UGM: {
      desc: "Universitas Gadjah Mada, a top educational icon in Yogyakarta.",
      img: "assets/images/tugu.jpg",
      coords: [-7.7694, 110.3776],
    },
    Monjali: {
      desc: "Monumen Jogja Kembali, a museum commemorating Indonesia’s independence.",
      img: "assets/images/tugu.jpg",
      coords: [-7.7479, 110.3664],
    },
    Airport: {
      desc: "Yogyakarta International Airport (YIA).",
      img: "assets/images/tugu.jpg",
      coords: [-7.9054, 110.0534],
    },
  };

  // =========================
  // GENERATE DROPDOWN OPTIONS
  // =========================
  for (const place in locationData) {
    const option1 = document.createElement("option");
    option1.value = place;
    option1.textContent = place;
    originSelect.appendChild(option1);

    const option2 = document.createElement("option");
    option2.value = place;
    option2.textContent = place;
    destinationSelect.appendChild(option2);
  }

  // =========================
  // GENERATE DESTINATION CARDS
  // =========================
  const cardsContainer = document.getElementById("destination-cards");
  for (const [name, data] of Object.entries(locationData)) {
    const card = document.createElement("div");
    card.classList.add("card");
    card.innerHTML = `
      <img src="${data.img}" alt="${name}">
      <h3>${name}</h3>
      <p>${data.desc}</p>
    `;
    cardsContainer.appendChild(card);
  }

  // =========================
  // INITIALIZE LEAFLET MAP
  // =========================
  window.map = L.map("map").setView([-7.79, 110.366], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(window.map);

  // =========================
  // FIND ROUTE BUTTON ACTION
  // =========================
  findRouteBtn.addEventListener("click", async () => {
    const origin = originSelect.value;
    const destination = destinationSelect.value;

    if (!origin || !destination) {
      routeOutput.innerHTML =
        "<p style='color:red;'>Please select both origin and destination.</p>";
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
        <p><b>🛣️ Route:</b> ${route}</p>
        <p><b>📏 Distance:</b> ${distance} km</p>
        <div>
          <img src="${locationData[origin].img}" alt="${origin}">
          <img src="${locationData[destination].img}" alt="${destination}">
        </div>
      `;

      // Update map route
      if (window.map && locationData[origin] && locationData[destination]) {
        const start = locationData[origin].coords;
        const end = locationData[destination].coords;

        if (window.routeLine) window.map.removeLayer(window.routeLine);
        if (window.startMarker) window.map.removeLayer(window.startMarker);
        if (window.endMarker) window.map.removeLayer(window.endMarker);

        window.routeLine = L.polyline([start, end], { color: "blue", weight: 4 }).addTo(window.map);
        window.startMarker = L.marker(start).addTo(window.map).bindPopup(origin);
        window.endMarker = L.marker(end).addTo(window.map).bindPopup(destination);
        window.map.fitBounds([start, end]);
      }

    } catch (error) {
      routeOutput.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
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
      addMessage("Dei-GO", data.response || "Sorry, I didn’t understand that.");
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
    messageDiv.innerHTML = `<div class="bubble"><b>${sender}:</b> ${message}</div>`;
    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  // =========================
  // SIMPLE GRAPH VISUALIZATION (OPTIONAL)
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
