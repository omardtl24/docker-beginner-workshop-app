const API = window.API_URL || "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("app");
  root.innerHTML = `
    <div class="container">
      <div class="left">
        <h2>Add Person</h2>
        <form id="personForm">
          <label>Name</label><input name="name" required />
          <label>Email</label><input name="email" type="email" required />
          <label>Age</label><input name="age" type="number" min="0" max="150" required />
          <button type="submit">Submit</button>
        </form>
        <button id="clearBtn" style="margin-top: 8px;">Clear Table</button>
        <div id="msg"></div>
      </div>
      <div class="right">
        <h2>People</h2>
        <table id="peopleTable">
          <thead><tr><th>Name</th><th>Email</th><th>Age</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </div>
  `;

  const form = document.getElementById("personForm");
  const msg = document.getElementById("msg");
  const tbody = document.querySelector("#peopleTable tbody");
  const clearBtn = document.getElementById("clearBtn");

  async function fetchPeople() {
    try {
      const res = await fetch(`${API}/people/`);
      if (!res.ok) throw new Error("Fetch failed");
      const data = await res.json();
      tbody.innerHTML = data.map(p => `<tr>
        <td>${escapeHtml(p.name)}</td>
        <td>${escapeHtml(p.email)}</td>
        <td>${p.age}</td>
      </tr>`).join("");
    } catch (e) {
      console.error(e);
      msg.innerText = "Could not load people.";
    }
  }

  function escapeHtml(text) {
    return String(text)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    msg.innerText = "";
    const formData = new FormData(form);
    const payload = {
      name: formData.get("name").trim(),
      email: formData.get("email").trim(),
      age: Number(formData.get("age")),
    };

    try {
      const res = await fetch(`${API}/person/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        msg.innerText = `Error: ${err.detail || res.statusText}`;
        return;
      }
      form.reset();
      await fetchPeople();
      msg.innerText = "Saved!";
      setTimeout(() => msg.innerText = "", 2000);
    } catch {
      msg.innerText = "Submission failed.";
    }
  });

  clearBtn.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to delete all people?")) return;

    try {
      const res = await fetch(`${API}/people/`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to clear database");
      await fetchPeople();
      msg.innerText = "Database cleared!";
      setTimeout(() => msg.innerText = "", 2000);
    } catch (e) {
      console.error(e);
      msg.innerText = "Could not clear database.";
    }
  });

  // Initial load
  fetchPeople();
});
