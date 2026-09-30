/* ============================================================
   narration.js — turn a long story string into clean paragraphs.
   The backend narration is 300–500 words separated by blank lines.
   ============================================================ */
(function () {
  "use strict";

  const Paracosm = (window.Paracosm = window.Paracosm || {});

  /**
   * Split raw narration text into an array of paragraph strings.
   * Handles double newlines, single newlines, or one long block.
   */
  Paracosm.toParagraphs = function toParagraphs(raw) {
    const text = String(raw || "").trim();
    if (!text) return [];

    // Preferred: split on blank lines.
    let parts = text.split(/\n\s*\n/);

    // Fallback: some models return single newlines only.
    if (parts.length === 1) {
      parts = text.split(/\n+/);
    }

    // Last resort: one giant block → chunk by sentences into ~3 paragraphs.
    if (parts.length === 1) {
      const sentences = text.match(/[^.!?]+[.!?]+(\s|$)/g);
      if (sentences && sentences.length > 4) {
        const perPara = Math.ceil(sentences.length / 3);
        parts = [];
        for (let i = 0; i < sentences.length; i += perPara) {
          parts.push(sentences.slice(i, i + perPara).join("").trim());
        }
      }
    }

    return parts.map((p) => p.replace(/\s+/g, " ").trim()).filter(Boolean);
  };

  /**
   * Render paragraphs into a container element as <p> nodes (safe: textContent).
   */
  Paracosm.renderNarration = function renderNarration(container, raw) {
    container.textContent = "";
    const paragraphs = Paracosm.toParagraphs(raw);
    paragraphs.forEach((paragraph) => {
      const p = document.createElement("p");
      p.textContent = paragraph;
      container.appendChild(p);
    });
  };
})();
