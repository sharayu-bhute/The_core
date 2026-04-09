let locationData = "";

// ── Location toggle ──
const toggle = document.getElementById("locationToggle");
const manualInput = document.getElementById("manualLocation");

if (toggle) {
  toggle.addEventListener("change", () => {
    if (manualInput) {
      manualInput.style.display = toggle.checked ? "none" : "block";
    }
  });
}

// ── Get GPS location ──
function getLocation() {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      locationData = `${pos.coords.latitude.toFixed(5)}, ${pos.coords.longitude.toFixed(5)}`;
      const status = document.getElementById("locationStatus");
      if (status) {
        status.textContent = `✓ Location captured: ${locationData}`;
        status.style.color = "var(--success)";
      }
    },
    () => {
      alert("Location access denied");
    }
  );
}

// ── Submit issue ──
async function submitIssue() {
  const fileInput = document.getElementById("imageInput");
  const loading   = document.getElementById("loading");
  const result    = document.getElementById("result");

  if (!fileInput || !fileInput.files[0]) {
    alert("Please upload a photo");
    return;
  }

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);
  formData.append("description", "Issue reported");

  if (locationData) {
    const [lat, lon] = locationData.split(",");
    formData.append("latitude", lat);
    formData.append("longitude", lon);
    formData.append("address", locationData);
  }

  if (loading) loading.style.display = "flex";

  try {
    const res  = await fetch("/submit-issue", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (loading) loading.style.display = "none";

    if (result) {
      result.innerHTML = `<p style="color:green;">${data.message}</p>`;
    }

    // 🔥 FIX: redirect to dashboard
    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 1000);

  } catch (err) {
    if (loading) loading.style.display = "none";
    alert("Error submitting issue");
    console.error(err);
  }
}

// ── Load user complaints ──
async function loadIssues() {
  try {
    const res = await fetch("/my-complaints"); // ✅ FIX
    const data = await res.json();

    const container = document.getElementById("issues");
    if (!container) return;

    if (!data.length) return;

    container.innerHTML = data.map(issue => `
      <div style="border:1px solid #ccc; padding:10px; margin:10px;">
        <img src="/${issue.image_path}" width="200"><br>
        <h3>${issue.issue_type}</h3>
        <p>Status: ${issue.status}</p>
        <p>Assigned: ${issue.assigned_to || "Not Assigned"}</p>
      </div>
    `).join("");

  } catch (err) {
    console.log("Dashboard error:", err);
  }
}

// ── Logout ──
function logout() {
  fetch("/logout", { method: "POST" })
    .then(() => window.location.href = "/login")
    .catch(() => window.location.href = "/login");
}