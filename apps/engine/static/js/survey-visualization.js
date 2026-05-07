/* survey-answer.js */

function collectAnswers() {
  const blocks = document.querySelectorAll(".question-block");
  const answers = [];
  let valid = true;

  blocks.forEach((block) => {
    const questionId = block.dataset.questionId;
    const type = block.dataset.type;
    const errorEl = block.querySelector(".field-error");
    let value = null;

    if (type === "text") {
      value = block.querySelector("textarea").value.trim();
    } else if (type === "number") {
      const raw = block.querySelector('input[type="number"]').value;
      value = raw !== "" ? Number(raw) : null;
    } else if (type === "radio") {
      const checked = block.querySelector('input[type="radio"]:checked');
      value = checked ? [checked.value] : null;
    } else if (type === "checkbox") {
      const checked = [
        ...block.querySelectorAll('input[type="checkbox"]:checked'),
      ];
      value = checked.length > 0 ? checked.map((el) => el.value) : null;
    }

    // Required validation
    const isRequired = block.querySelector("[required]") !== null;
    const isEmpty = value === null || value === "";

    if (isRequired && isEmpty) {
      block.classList.add("has-error");
      errorEl.classList.remove("hidden");
      valid = false;
    } else {
      block.classList.remove("has-error");
      errorEl.classList.add("hidden");
    }

    // Wrap text and single-value types in array to match schema,
    // or keep number as-is
    let formatted;
    if (type === "text") {
      formatted = value; // plain string
    } else if (type === "number") {
      formatted = value; // plain number
    } else {
      formatted = value ?? []; // array (radio / checkbox)
    }

    answers.push({ question_id: questionId, value: formatted });
  });

  return { valid, answers };
}

function setNote(msg, isError = false) {
  const el = document.getElementById("footer-note");
  el.textContent = msg;
  el.className = isError ? "error" : "";
}

function submitSurvey() {
  const { valid, answers } = collectAnswers();

  if (!valid) {
    setNote("Please answer all required questions.", true);
    // scroll to first error
    const first = document.querySelector(".question-block.has-error");
    if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  const surveyId = Number(
    document.getElementById("survey-form").dataset.surveyId,
  );
  const payload = { survey_id: surveyId, answers };

  setNote("Submitting…");

  fetch(`/api/submission/${surveyId}/`, {
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
        setNote("Something went wrong. Please try again.", true);
      }
    })
    .catch(() => {
      setNote("Network error. Please try again.", true);
    });
}

function getCookie(name) {
  const match = document.cookie.match(
    new RegExp("(?:^|; )" + name + "=([^;]*)"),
  );
  return match ? decodeURIComponent(match[1]) : null;
}
