/* ============================================================
   api.js — the only place the frontend talks to the backend.
   No API keys ever live here. The Python backend holds them.
   ============================================================ */
(function () {
  "use strict";

  const Paracosm = (window.Paracosm = window.Paracosm || {});

  // Backend base URL. Override by setting window.PARACOSM_API before scripts load.
  Paracosm.API_BASE = window.PARACOSM_API || "http://localhost:8080";
  Paracosm.ENDPOINT = "/api/generate-reality";

  /**
   * Ask the backend to build an alternate reality.
   * @param {string} prompt
   * @returns {Promise<{reality:Object, imagePrompts:string[], images:string[]}>}
   */
  Paracosm.generateReality = async function generateReality(prompt) {
    const url = Paracosm.API_BASE + Paracosm.ENDPOINT;

    let response;
    try {
      response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
    } catch (networkError) {
      // Backend not running / unreachable / CORS blocked.
      throw new Error(
        "Cannot reach the PARACOSM backend at " +
          Paracosm.API_BASE +
          ". Start the Python server (START-PARACOSM.command) and try again."
      );
    }

    let data = null;
    try {
      data = await response.json();
    } catch (_) {
      data = null;
    }

    if (!response.ok) {
      const detail =
        (data && (data.error || data.detail)) ||
        "The backend returned an error (" + response.status + ").";
      throw new Error(
        typeof detail === "string" ? detail : JSON.stringify(detail)
      );
    }

    if (!data || !data.reality) {
      throw new Error("The backend returned an empty reality.");
    }

    return data;
  };
})();
