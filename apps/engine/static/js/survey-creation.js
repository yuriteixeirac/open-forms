/* survey-creation.js */

let questions = [];
let selectedType = "text";
let nextId = 1;

/* ─── Type selector ─────────────────────────────────────────── */
document.querySelectorAll(".type-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document
      .querySelectorAll(".type-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedType = btn.dataset.type;
  });
});

/* ─── Add field ─────────────────────────────────────────────── */
function addField() {
  const id = nextId++;
  const q = {
    id,
    type: selectedType,
    question: "",
    required: false,
    options: [],
  };

  if (selectedType === "radio" || selectedType === "checkbox") {
    q.options = ["", ""]; // start with two empty options
  }

  questions.push(q);
  renderCard(q);
  updateCount();
  updateEmptyState();
}

/* ─── Render a single card ───────────────────────────────────── */
function renderCard(q) {
  const container = document.getElementById("survey-fields");
  const index = questions.findIndex((x) => x.id === q.id);

  const card = document.createElement("div");
  card.className = "question-card";
  card.dataset.id = q.id;

  const hasOptions = q.type === "radio" || q.type === "checkbox";
  const bulletClass =
    q.type === "checkbox" ? "option-bullet square" : "option-bullet";

  card.innerHTML = `
        <div class="card-top">
            <div class="card-index">${String(index + 1).padStart(2, "0")}</div>
            <div class="card-body">
                <input
                    class="question-input"
                    type="text"
                    placeholder="Type your question here…"
                    value="${escHtml(q.question)}"
                    oninput="updateQuestion(${q.id}, 'question', this.value)"
                >
                <div class="card-meta">
                    <span class="type-badge" data-type="${q.type}">${q.type}</span>
                    <label class="required-toggle">
                        <input
                            type="checkbox"
                            ${q.required ? "checked" : ""}
                            onchange="updateQuestion(${q.id}, 'required', this.checked)"
                        >
                        <span class="required-label">Required</span>
                    </label>
                </div>
                ${
                  hasOptions
                    ? `
                <div class="options-list" id="options-${q.id}">
                    <div class="options-label">Options</div>
                    ${q.options.map((opt, i) => optionRowHtml(q.id, i, opt, bulletClass)).join("")}
                    <button class="add-option-btn" onclick="addOption(${q.id})">+ Add option</button>
                </div>`
                    : ""
                }
            </div>
            <button class="delete-btn" onclick="deleteField(${q.id})" title="Remove question">✕</button>
        </div>
    `;

  container.appendChild(card);
}

function optionRowHtml(qId, index, value, bulletClass) {
  return `
        <div class="option-row" data-index="${index}">
            <div class="${bulletClass}"></div>
            <input
                class="option-input"
                type="text"
                placeholder="Option label…"
                value="${escHtml(value)}"
                oninput="updateOption(${qId}, ${index}, this.value)"
            >
            <button class="remove-option-btn" onclick="removeOption(${qId}, ${index})" title="Remove option">✕</button>
        </div>
    `;
}

/* ─── Mutations ─────────────────────────────────────────────── */
function updateQuestion(id, key, value) {
  const q = questions.find((x) => x.id === id);
  if (q) q[key] = value;
}

function updateOption(qId, index, value) {
  const q = questions.find((x) => x.id === qId);
  if (q) q.options[index] = value;
}

function addOption(qId) {
  const q = questions.find((x) => x.id === qId);
  if (!q) return;
  const newIndex = q.options.length;
  q.options.push("");

  const bulletClass =
    q.type === "checkbox" ? "option-bullet square" : "option-bullet";
  const list = document.getElementById(`options-${qId}`);
  const addBtn = list.querySelector(".add-option-btn");
  const row = document.createElement("div");
  row.innerHTML = optionRowHtml(qId, newIndex, "", bulletClass);
  list.insertBefore(row.firstElementChild, addBtn);
  list
    .querySelector(`.option-row[data-index="${newIndex}"] .option-input`)
    .focus();
}

function removeOption(qId, index) {
  const q = questions.find((x) => x.id === qId);
  if (!q || q.options.length <= 1) return;

  q.options.splice(index, 1);

  // re-render options list content only
  const bulletClass =
    q.type === "checkbox" ? "option-bullet square" : "option-bullet";
  const list = document.getElementById(`options-${qId}`);
  list.innerHTML =
    `<div class="options-label">Options</div>` +
    q.options
      .map((opt, i) => optionRowHtml(qId, i, opt, bulletClass))
      .join("") +
    `<button class="add-option-btn" onclick="addOption(${qId})">+ Add option</button>`;
}

function deleteField(id) {
  questions = questions.filter((x) => x.id !== id);
  const card = document.querySelector(`.question-card[data-id="${id}"]`);
  if (card) {
    card.style.transition = "opacity 0.15s, transform 0.15s";
    card.style.opacity = "0";
    card.style.transform = "translateY(-6px)";
    setTimeout(() => {
      card.remove();
      reIndexCards();
    }, 150);
  }
  updateCount();
  updateEmptyState();
}

function reIndexCards() {
  document.querySelectorAll(".question-card").forEach((card, i) => {
    card.querySelector(".card-index").textContent = String(i + 1).padStart(
      2,
      "0",
    );
  });
}

/* ─── UI helpers ─────────────────────────────────────────────── */
function updateCount() {
  const n = questions.length;
  document.getElementById("questions-count").textContent =
    n === 0 ? "0 questions" : `${n} question${n > 1 ? "s" : ""}`;
}

function updateEmptyState() {
  const empty = document.getElementById("empty-state");
  empty.classList.toggle("hidden", questions.length > 0);
}

function setNote(msg, isError = false) {
  const el = document.getElementById("footer-note");
  el.textContent = msg;
  el.className = "footer-note" + (isError ? " error" : "");
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ─── Build JSON & submit ────────────────────────────────────── */
function buildAndSubmit() {
  const name = document.getElementById("survey-name").value.trim();
  const description = document
    .getElementById("survey-description")
    .value.trim();
  const deadlineRaw = document.getElementById("survey-deadline").value;
  const deadline = deadlineRaw ? new Date(deadlineRaw).toISOString() : null;

  if (!name) {
    setNote("Survey name is required.", true);
    return;
  }
  if (!deadline) {
    setNote("Please set a valid until date.", true);
    return;
  }
  if (new Date(deadlineRaw) <= new Date()) {
    setNote("Valid until must be in the future.", true);
    return;
  }
  if (questions.length === 0) {
    setNote("Add at least one question.", true);
    return;
  }

  const builtQuestions = [];
  for (const q of questions) {
    if (!q.question.trim()) {
      setNote("All questions must have text.", true);
      return;
    }

    const entry = { question: q.question.trim(), type: q.type };

    if (q.type === "radio" || q.type === "checkbox") {
      const opts = q.options.map((o) => o.trim()).filter(Boolean);
      if (opts.length < 2) {
        setNote(`A ${q.type} question needs at least 2 options.`, true);
        return;
      }
      entry.options = opts;
    }

    if (q.required) entry.required = true;

    builtQuestions.push(entry);
  }

  const payload = {
    name,
    description,
    valid_until: deadline,
    questions: builtQuestions,
  };

  setNote("Sending…");

  fetch("/api/survey/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(payload),
  })
    .then((r) => {
      if (r.ok) {
        window.location.href = "/";
      } else {
        window.location.href = "/engine/survey";
      }
    })
    .catch(() => {
      window.location.href = "/engine/survey";
    });
}

// Helper for CSRF token when you hook up the fetch
function getCookie(name) {
  const match = document.cookie.match(
    new RegExp("(?:^|; )" + name + "=([^;]*)"),
  );
  return match ? decodeURIComponent(match[1]) : null;
}
