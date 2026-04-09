let locationData = "";

const toggle = document.getElementById("locationToggle");
const manualInput = document.getElementById("manualLocation");

if (toggle) {
  toggle.addEventListener("change", () => {
    manualInput.style.display = toggle.checked ? "none" : "block";
  });
}

function getLocation() {
  navigator.geolocation.getCurrentPosition((pos) => {
    locationData = `${pos.coords.latitude}, ${pos.coords.longitude}`;
    alert("Location fetched");
  }, () => {
    alert("Location access denied");
  });
}

async function submitIssue() {
  const file = document.getElementById("imageInput").files[0];
  const loading = document.getElementById("loading");
  const result = document.getElementById("result");

  if (!file) {
    alert("Please upload an image");
    return;
  }

  if (!toggle.checked) {
    locationData = manualInput.value;
  }

  const formData = new FormData();
  formData.append("image", file);
  formData.append("location", locationData);

  loading.innerHTML = "Processing image...";
  result.innerHTML = "";

  try {
    const res = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    loading.innerHTML = "";

    result.innerHTML = `
      <div class="card">
        <h3>Detected Issue: ${data.issue_type}</h3>
        <p>Department: ${data.department}</p>
      </div>
    `;
  } catch (err) {
    loading.innerHTML = "";
    alert("Error submitting issue");
  }
}

// Dashboard (will work only after backend API exists)
async function loadIssues() {
  try {
    const res = await fetch("/complaints");
    const data = await res.json();

    const container = document.getElementById("issues");

    container.innerHTML = data.map(issue => `
      <div class="card">
        <img src="${issue.image_path}" width="200">
        <h3>${issue.issue_type}</h3>
        <p>Status: ${issue.status}</p>
        <p>Assigned: ${issue.assigned_to || "Not Assigned"}</p>
      </div>
    `).join("");

  } catch (err) {
    console.log("Dashboard not ready (backend missing)");
  }
}