// ===============================
// DEI-GO Smart Route Assistant
// ===============================

document.addEventListener("DOMContentLoaded", () => {
  // -------------------------------
  // ELEMENTS
  // -------------------------------
  const routeOutput = document.getElementById("route-output");
  const originSelect = document.getElementById("origin");
  const destinationSelect = document.getElementById("destination");
  const findRouteBtn = document.getElementById("find-route-btn");

  const chatOutput = document.getElementById("chatbox");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // -------------------------------
  // LOCATION DATA
  // -------------------------------
  const locations = {
    "Tugu Jogja": {
      desc: "A historical landmark in the heart of Yogyakarta.",
      img: "static/images/tugu.jpg",
      coords: [-7.7829, 110.3671],
    },
    Malioboro: {
      desc: "The most famous shopping street in Yogyakarta.",
      img: "static/images/malioboro.jpg",
      coords: [-7.793, 110.3658],
    },
    Keraton: {
      desc: "The magnificent Sultan’s Palace.",
      img: "static/images/keraton.jpg",
      coords: [-7.8056, 110.3649],
    },
    "Alun-Alun Kidul": {
      desc: "A popular night attraction in Yogyakarta.",
      img: "static/images/alun.jpg",
      coords: [-7.8111, 110.3643],
    },
    UGM: {
      desc: "Universitas Gadjah Mada, a top educational icon in Yogyakarta.",
      img: "static/images/ugm.jpg",
      coords: [-7.7694, 110.3776],
    },
    Monjali: {
      desc: "Monumen Jogja Kembali, a museum commemorating Indonesia’s independence.",
      img: "static/images/monjali.jpg",
      coords: [-7.7479, 110.3664],
    },
    Bandara: {
      desc: "Yogyakarta International Airport (YIA).",
      img: "static/images/bandara.jpg",
      coords: [-7.9054, 110.0534],
    },
  };

  // -------------------------------
  // POPULATE DROPDOWN OPTIONS
  // -------------------------------
  Object.keys(locations).forEach((name) => {
    originSelect.innerHTML += `<option value="${name}">${name}</option>`;
    destinationSelect.innerHTML += `<option value="${name}">${name}</option>`;
  });

  // -------------------------------
  // DESTINATION CARDS
  // -------------------------------
  const cardsContainer = document.getElementById("destination-cards");
  for (const [name, data] of Object.entries(locations)) {
    cardsContainer.innerHTML += `
      <div class="card fade-in">
        <img src="${data.img}" alt="${name}">
        <h3>${name}</h3>
        <p>${data.desc}</p>
      </div>`;
  }

  // -------------------------------
  // LEAFLET MAP SETUP
  // -------------------------------
  const map = L.map("map").setView([-7.79, 110.366], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  }).addTo(map);

  let routeLine, startMarker, endMarker;

  // -------------------------------
  // FIND ROUTE FUNCTION
  // -------------------------------
  findRouteBtn.addEventListener("click", async () => {
    const start = originSelect.value;
    const end = destinationSelect.value;

    if (!start || !end) {
      routeOutput.innerHTML = "<p style='color:red;'>⚠️ Please select both locations.</p>";
      return;
    }
    if (start === end) {
      routeOutput.innerHTML = "<p style='color:red;'>❌ Start and destination cannot be the same!</p>";
      return;
    }

    try {
      const res = await fetch("/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start, end }),
      });
      const data = await res.json();

      if (data.error) throw new Error(data.error);

      routeOutput.innerHTML = `
        <div class="fade-in">
          <p><b>🛣️ Route:</b> ${data.route.join(" → ")}</p>
          <p><b>📏 Distance:</b> ${data.distance} km</p>
          <div class="route-images">
            <img src="${locations[start].img}" alt="${start}">
            <img src="${locations[end].img}" alt="${end}">
          </div>
        </div>
      `;

      const startC = locations[start].coords;
      const endC = locations[end].coords;

      [routeLine, startMarker, endMarker].forEach((m) => m && map.removeLayer(m));
      routeLine = L.polyline([startC, endC], { color: "blue", weight: 4 }).addTo(map);
      startMarker = L.marker(startC).addTo(map).bindPopup(`<b>${start}</b>`);
      endMarker = L.marker(endC).addTo(map).bindPopup(`<b>${end}</b>`);
      map.fitBounds([startC, endC]);

    } catch (err) {
      routeOutput.innerHTML = `<p style="color:red;">⚠️ Error: ${err.message}</p>`;
    }
  });

  // -------------------------------
  // CHATBOT SECTION
  // -------------------------------
  function addMessage(sender, text) {
    const div = document.createElement("div");
    div.classList.add(sender === "You" ? "user-message" : "bot-message", "fade-in");
    div.innerHTML = `<div class="bubble"><b>${sender}:</b> ${text}</div>`;
    chatOutput.appendChild(div);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("You", message);
    userInput.value = "";

    try {
      const res = await fetch("/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: message }),
      });
      const data = await res.json();

      addMessage("Dei-GO", data.response || "Hmm... I'm not sure I understand 🤔");
    } catch {
      addMessage("Dei-GO", "⚠️ Server error. Please try again later.");
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // -------------------------------
  // SMALL UI TOUCH: FADE-IN ANIMATION
  // -------------------------------
  const style = document.createElement("style");
  style.textContent = `
    .fade-in { animation: fadeIn 0.5s ease-in; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `;
  document.head.appendChild(style);
});
