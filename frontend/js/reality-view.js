/* ============================================================
   reality-view.js — loading choreography, error display,
   and rendering the full alternate-reality dossier.
   ============================================================ */
(function () {
  "use strict";

  const Paracosm = (window.Paracosm = window.Paracosm || {});
  const $ = (id) => document.getElementById(id);

  const els = {
    resultZone: $("resultZone"),
    loading: $("loading"),
    loadingStage: $("loadingStage"),
    loadingSub: $("loadingSub"),
    loadingFill: $("loadingFill"),
    result: $("result"),
    error: $("error"),
    scrollHint: $("scrollHint"),
    // result fields
    probability: $("probability"),
    title: $("title"),
    divergence: $("divergence"),
    summary: $("summary"),
    narration: $("narration"),
    timeline: $("timeline"),
    timelineWrap: $("timelineWrap"),
    selfGrid: $("selfGrid"),
    selfWrap: $("selfWrap"),
    worldChanges: $("worldChanges"),
    consequences: $("consequences"),
  };

  const STAGES = [
    { t: "Splitting the timeline",       s: "Holding your question steady while the world begins to rearrange itself." },
    { t: "Mapping the divergence",       s: "Tracing the exact point where this reality breaks away from ours." },
    { t: "Building consequences",        s: "Following every change outward, one year leading into the next." },
    { t: "Rendering alternate memories", s: "Composing the scenes that could not exist until this moment." },
    { t: "Generating images",            s: "Developing three photographs from a world that never happened." },
  ];

  let stageTimer = null;

  /* ---------- Loading choreography ---------- */
  function startLoading() {
    clearError();
    els.result.classList.remove("active");
    els.loading.classList.add("active");

    let i = 0;
    const total = STAGES.length;
    const paint = () => {
      const stage = STAGES[Math.min(i, total - 1)];
      els.loadingStage.textContent = stage.t;
      els.loadingSub.textContent = stage.s;
      // cap progress at ~90% until the real result arrives
      const pct = Math.min(90, Math.round(((i + 1) / total) * 90));
      els.loadingFill.style.width = pct + "%";
      i += 1;
    };
    paint();
    stageTimer = setInterval(() => {
      if (i >= total) {
        // linger on the final stage; nudge the bar gently
        const current = parseFloat(els.loadingFill.style.width) || 90;
        els.loadingFill.style.width = Math.min(92, current + 0.4) + "%";
        return;
      }
      paint();
    }, 2600);
  }

  function stopLoading() {
    if (stageTimer) clearInterval(stageTimer);
    stageTimer = null;
    els.loadingFill.style.width = "100%";
    setTimeout(() => els.loading.classList.remove("active"), 260);
  }

  /* ---------- Errors ---------- */
  function showError(message) {
    if (stageTimer) clearInterval(stageTimer);
    stageTimer = null;
    els.loading.classList.remove("active");
    els.error.textContent = message || "Something went wrong.";
    els.error.classList.add("active");
  }
  function clearError() {
    els.error.textContent = "";
    els.error.classList.remove("active");
  }

  /* ---------- Small DOM helpers ---------- */
  function card(title, desc) {
    const wrap = document.createElement("div");
    wrap.className = "card";
    const t = document.createElement("div");
    t.className = "c-title";
    t.textContent = title || "";
    const d = document.createElement("div");
    d.className = "c-desc";
    d.textContent = desc || "";
    wrap.append(t, d);
    return wrap;
  }

  function fillCards(container, items) {
    container.textContent = "";
    (items || []).forEach((it) => {
      if (!it) return;
      container.appendChild(card(it.title, it.description));
    });
  }

  /* ---------- Images ---------- */
  function loadImage(index, url, caption) {
    const box = $("img" + index);
    const cap = $("cap" + index);
    if (cap) cap.textContent = caption || "";
    if (!box) return;

    box.className = "frame-img loading-shimmer";
    box.style.backgroundImage = "";

    if (!url) {
      box.className = "frame-img failed";
      return;
    }

    const probe = new Image();
    probe.onload = () => {
      box.style.backgroundImage = 'url("' + url + '")';
      box.className = "frame-img";
    };
    probe.onerror = () => {
      box.className = "frame-img failed";
    };
    probe.src = url;
  }

  /* ---------- Caption text from the reality ---------- */
  function caption(reality, index) {
    const scenes = Array.isArray(reality.visualScenes) ? reality.visualScenes : [];
    const scene = scenes[index];
    if (typeof scene === "string" && scene.trim()) {
      // trim to a tidy single sentence-ish caption
      const clean = scene.replace(/\s+/g, " ").trim();
      return clean.length > 150 ? clean.slice(0, 147).trim() + "…" : clean;
    }
    return "";
  }

  /* ---------- Render the full dossier ---------- */
  function renderResult(data) {
    const reality = data.reality || {};
    const images = Array.isArray(data.images) ? data.images : [];

    els.probability.textContent = "Probability · " + (reality.probability || "Unknown");
    els.title.textContent = reality.realityName || "An Alternate Reality";
    els.divergence.textContent = reality.divergencePoint || "";
    els.summary.textContent = reality.summary || "";

    Paracosm.renderNarration(els.narration, reality.narration);

    // Images + captions
    for (let i = 0; i < 3; i++) {
      loadImage(i, images[i], caption(reality, i));
    }

    // Timeline
    els.timeline.textContent = "";
    const timeline = Array.isArray(reality.timeline) ? reality.timeline : [];
    if (timeline.length) {
      timeline.forEach((row) => {
        const li = document.createElement("li");
        const y = document.createElement("div");
        y.className = "t-year";
        y.textContent = row.year || "";
        const e = document.createElement("div");
        e.className = "t-event";
        e.textContent = row.event || "";
        li.append(y, e);
        els.timeline.appendChild(li);
      });
      els.timelineWrap.style.display = "";
    } else {
      els.timelineWrap.style.display = "none";
    }

    // Alternate self
    const self = reality.alternateSelf || {};
    els.selfGrid.textContent = "";
    const selfRows = [
      ["Role", self.role],
      ["Location", self.location],
      ["Relationships", self.relationships],
      ["Inner conflict", self.innerConflict],
    ].filter((r) => r[1]);
    if (selfRows.length) {
      selfRows.forEach(([k, v]) => {
        const cell = document.createElement("div");
        cell.className = "self-cell";
        const key = document.createElement("div");
        key.className = "s-key";
        key.textContent = k;
        const val = document.createElement("div");
        val.className = "s-val";
        val.textContent = v;
        cell.append(key, val);
        els.selfGrid.appendChild(cell);
      });
      els.selfWrap.style.display = "";
    } else {
      els.selfWrap.style.display = "none";
    }

    // World changes + long-term consequences
    fillCards(els.worldChanges, reality.worldChanges);
    fillCards(els.consequences, reality.longTermConsequences);

    stopLoading();
    els.result.classList.add("active");
    if (els.scrollHint) els.scrollHint.hidden = false;
  }

  /* ---------- Public surface ---------- */
  Paracosm.view = {
    startLoading,
    stopLoading,
    showError,
    clearError,
    renderResult,
    scrollToResult() {
      els.resultZone.scrollIntoView({ behavior: "smooth", block: "start" });
    },
  };
})();
