// let locationData = "";

// const toggle = document.getElementById("locationToggle");
// const manualInput = document.getElementById("manualLocation");

// if (toggle) {
//   toggle.addEventListener("change", () => {
//     manualInput.style.display = toggle.checked ? "none" : "block";
//   });
// }

// function getLocation() {
//   navigator.geolocation.getCurrentPosition((pos) => {
//     locationData = `${pos.coords.latitude}, ${pos.coords.longitude}`;
//     alert("Location fetched");
//   }, () => {
//     alert("Location access denied");
//   });
// }

// async function submitIssue() {
//   const file = document.getElementById("imageInput").files[0];
//   const loading = document.getElementById("loading");
//   const result = document.getElementById("result");

//   if (!file) {
//     alert("Please upload an image");
//     return;
//   }

//   if (!toggle.checked) {
//     locationData = manualInput.value;
//   }

//   const formData = new FormData();
//   formData.append("image", file);
//   formData.append("location", locationData);

//   loading.innerHTML = "Processing image...";
//   result.innerHTML = "";

//   try {
//     const res = await fetch("/upload", {
//       method: "POST",
//       body: formData
//     });

//     const data = await res.json();

//     loading.innerHTML = "";

//     result.innerHTML = `
//       <div class="card">
//         <h3>Detected Issue: ${data.issue_type}</h3>
//         <p>Department: ${data.department}</p>
//       </div>
//     `;
//   } catch (err) {
//     loading.innerHTML = "";
//     alert("Error submitting issue");
//   }
// }

// // Dashboard (will work only after backend API exists)
// async function loadIssues() {
//   try {
//     const res = await fetch("/complaints");
//     const data = await res.json();

//     const container = document.getElementById("issues");

//     container.innerHTML = data.map(issue => `
//       <div class="card">
//         <img src="${issue.image_path}" width="200">
//         <h3>${issue.issue_type}</h3>
//         <p>Status: ${issue.status}</p>
//         <p>Assigned: ${issue.assigned_to || "Not Assigned"}</p>
//       </div>
//     `).join("");

//   } catch (err) {
//     console.log("Dashboard not ready (backend missing)");
//   }
// }






/* ===========================
   SAMADHAN — app.js
   Handles issue upload + dashboard
   =========================== */

let locationData = "";

// ── Location toggle (upload page) ──
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
      } else {
        showToast("📍 Location captured successfully", "success");
      }
    },
    () => {
      showToast("Location access denied — enter address manually.", "error");
    }
  );
}

// ── Submit issue ──
async function submitIssue() {
  const fileInput = document.getElementById("imageInput");
  const loading   = document.getElementById("loading");
  const result    = document.getElementById("result");

  if (!fileInput || !fileInput.files[0]) {
    showToast("Please upload a photo of the issue.", "error");
    return;
  }

  const useGPS    = toggle ? toggle.checked : false;
  const finalLoc  = useGPS ? locationData : (manualInput ? manualInput.value : "");

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);
  formData.append("location", finalLoc);

  if (loading) { loading.style.display = "flex"; }
  if (result)  { result.innerHTML = ""; }

  try {
    const res  = await fetch("/upload", { method: "POST", body: formData });
    const data = await res.json();

    if (loading) { loading.style.display = "none"; }

    if (result) {
      result.innerHTML = `
        <div class="card" style="margin-top:1rem;border-left:3px solid var(--success);">
          <div class="card-header">
            <div>
              <div class="card-title">✅ Issue Submitted</div>
              <div class="card-meta" style="margin-top:0.25rem;">Classified and routed automatically</div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.5rem;font-size:0.875rem;">
            <div>
              <span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Issue Type</span>
              <p style="margin-top:0.15rem;font-weight:600;">${data.issue_type || "Unclassified"}</p>
            </div>
            <div>
              <span style="color:var(--text-muted);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Department</span>
              <p style="margin-top:0.15rem;font-weight:600;">${data.department || "—"}</p>
            </div>
          </div>
          <a href="/dashboard" style="display:inline-flex;align-items:center;gap:0.4rem;margin-top:1rem;font-size:0.875rem;font-weight:600;color:var(--accent-2);">
            View in dashboard →
          </a>
        </div>
      `;
    }
  } catch (err) {
    if (loading) { loading.style.display = "none"; }
    showToast("Failed to submit — please try again.", "error");
    console.error(err);
  }
}

// ── Load issues (user dashboard) ──
async function loadIssues() {
  try {
    const res       = await fetch("/complaints");
    const data      = await res.json();
    const container = document.getElementById("issues");
    if (!container) return;

    if (!data || !data.length) {
      // Empty state handled in HTML
      return;
    }

    // Update stats if elements exist
    const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setEl("statTotal",    data.length);
    setEl("statPending",  data.filter(i => (i.status||"").toLowerCase() === "pending").length);
    setEl("statResolved", data.filter(i => (i.status||"").toLowerCase() === "resolved").length);

    const emptyState = document.getElementById("emptyState");
    if (emptyState) emptyState.style.display = "none";

    const statusBadge = (status) => {
      const map = { pending:"badge-pending", assigned:"badge-assigned", resolved:"badge-resolved", rejected:"badge-rejected" };
      const cls = map[(status||"").toLowerCase()] || "badge-pending";
      return `<span class="badge ${cls}">${status || "Pending"}</span>`;
    };

    container.innerHTML = data.map((issue, idx) => `
      <div class="card reveal" style="animation-delay:${idx * 0.06}s">
        ${issue.image_path
          ? `<img src="${issue.image_path}" alt="${issue.issue_type || "Issue"}">`
          : ""}
        <div class="card-header">
          <div>
            <div class="card-title">${issue.issue_type || "Unclassified"}</div>
            <div class="card-meta" style="margin-top:0.2rem;">${issue.location || ""}</div>
          </div>
          ${statusBadge(issue.status)}
        </div>
        <div style="font-size:0.8rem;color:var(--text-muted);">
          ${issue.assigned_to
            ? `Assigned to: <strong>${issue.assigned_to}</strong>`
            : "Not yet assigned"}
        </div>
      </div>
    `).join("");

    // Scroll reveal
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); } });
    }, { threshold: 0.1 });
    document.querySelectorAll(".card.reveal").forEach(el => io.observe(el));

  } catch (err) {
    console.log("Dashboard not ready (backend missing):", err);
  }
}

// ── Auth logout ──
function logout() {
  fetch("/logout", { method: "POST" })
    .then(() => window.location.href = "/login")
    .catch(() => window.location.href = "/login");
}

// ── Toast notifications ──
function showToast(message, type = "info") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;

  const colors = {
    success: { bg: "#E8F5EE", color: "#1D7D4F", border: "#A8D8BB" },
    error:   { bg: "#FBEAEA", color: "#C42B2B", border: "#E8B0B0" },
    info:    { bg: "#EAF0FB", color: "#1A5CD4", border: "#A8BFE8" }
  };
  const c = colors[type] || colors.info;

  Object.assign(toast.style, {
    position: "fixed",
    bottom: "1.5rem",
    right: "1.5rem",
    background: c.bg,
    color: c.color,
    border: `1px solid ${c.border}`,
    borderRadius: "8px",
    padding: "0.85rem 1.25rem",
    fontSize: "0.875rem",
    fontWeight: "500",
    fontFamily: "'DM Sans', sans-serif",
    boxShadow: "0 4px 16px rgba(0,0,0,0.12)",
    zIndex: "9999",
    maxWidth: "340px",
    animation: "fadeUp 0.3s ease forwards"
  });

  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}