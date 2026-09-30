/* ============================================================
   app.js — form + suggestion controller. Wires the UI to the
   API and the view. Loaded last (all deps already defined).
   ============================================================ */
(function () {
  "use strict";

  const Paracosm = window.Paracosm || {};
  const view = Paracosm.view;

  const form = document.getElementById("form");
  const input = document.getElementById("prompt");
  const submit = form.querySelector(".submit");
  const suggestions = document.getElementById("suggestions");
  const again = document.getElementById("again");
  const errorEl = document.getElementById("error");

  let busy = false;

  function setBusy(state) {
    busy = state;
    submit.disabled = state;
    input.disabled = state;
  }

  async function generate(rawPrompt) {
    const prompt = (rawPrompt || "").trim();

    // client-side validation mirrors the backend rules
    if (prompt.length < 8) {
      errorEl.textContent = "Ask a slightly fuller question — at least 8 characters.";
      errorEl.classList.add("active");
      input.focus();
      return;
    }
    if (prompt.length > 500) {
      errorEl.textContent = "That question is too long. Keep it under 500 characters.";
      errorEl.classList.add("active");
      return;
    }

    setBusy(true);
    view.clearError();
    view.startLoading();
    view.scrollToResult();

    try {
      const data = await Paracosm.generateReality(prompt);
      view.renderResult(data);
    } catch (err) {
      view.showError(err && err.message ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (busy) return;
    generate(input.value);
  });

  suggestions.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn || busy) return;
    input.value = btn.textContent.trim();
    generate(input.value);
  });

  if (again) {
    again.addEventListener("click", () => {
      document.getElementById("hero").scrollIntoView({ behavior: "smooth", block: "start" });
      setTimeout(() => input.focus(), 400);
    });
  }
})();
