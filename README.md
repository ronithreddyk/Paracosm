# PARACOSM — Alternate Reality Simulator

Ask one impossible question.

PARACOSM doesn't give you the obvious answer. It searches for the strange one.

Give it a *what if?* and it builds an alternate reality around it — not just a generic prediction, but a specific world shaped by unexpected consequences, strange details, and events that unfold from your question.

Every simulation creates a named reality, a cinematic 300–500 word narration, a causal timeline showing how the world diverged, your alternate self within that reality, long-term consequences, and three AI-generated photographs that look like memories from a life that never happened.

The same kind of question can lead somewhere completely different every time. Some realities are fascinating. Some are disturbing. Some are ridiculous.

That's the point.

PARACOSM isn't trying to tell you what *would* happen.

It's showing you what **could have happened in a reality stranger than ours.**

```text
What if Messi was kidnapped before the World Cup final?

What if Earth had two moons?

What if the oceans floated above us instead of covering the Earth?

What if humans discovered something beneath Antarctica that was never supposed to be found?

What if you woke up tomorrow and everyone remembered a version of you that never existed?
```

**One question. One divergence. An entirely different reality.**

## Demo

![PARACOSM demo — one impossible question to a fully rendered alternate world](assets/paracosm-demo.gif)

> **▶ [Watch in full quality with sound](assets/paracosm-demo.mp4)** — the same walkthrough in HD.

<!--
  The GIF above plays automatically on GitHub — no click needed.
  For an even sharper inline player (optional), GitHub can embed a video uploaded through its UI:
    1. Edit this README on github.com (or open a new draft Issue).
    2. Drag assets/paracosm-demo.mp4 into the editor and wait for the upload to finish.
    3. GitHub inserts a URL like https://github.com/user-attachments/assets/xxxxxxxx
    4. Paste that URL on its own blank line and remove the GIF line above if you prefer the HD player.
-->

## Screenshots

|  |  |
| --- | --- |
| **The doorway** — every world starts with one impossible question | **Building the world** — the rift traces where this reality breaks from ours |
| ![Landing screen](assets/01-landing.png) | ![Generating screen](assets/02-generating.png) |

**The dossier** — a named world with a probability rating

![Result — The Stratos-Oceanic Earth](assets/03-result-hero.png)

**Three photographs from a world that never happened** — the moment reality changed, life inside the new reality, and its long-term consequence

![Generated reality images and narration](assets/04-reality-images.png)

**A causal timeline and your alternate self**

![Timeline and alternate self](assets/05-timeline-alternate-self.png)

## Architecture

The frontend never touches an API key. It only talks to your local backend, which holds the
secrets and calls the AI services on your behalf.

```
Browser (frontend)
   │  POST /api/generate-reality  { prompt }
   ▼
FastAPI backend  ──►  Gemini        (structured reality JSON, length-enforced narration)
                 ──►  Pollinations  (three images from scene prompts)
   │  { reality, imagePrompts, images }
   ▼
Browser renders the dossier
```

## Project layout

```
paracosm/
├── START-PARACOSM.command  One-click launcher (macOS)
├── assets/                 README media (demo GIF + video + screenshots)
├── backend/
│   ├── main.py                 FastAPI app, CORS, static image serving
│   ├── app/
│   │   ├── models.py           Request/response schemas + validation
│   │   ├── services.py         Gemini + Pollinations orchestration
│   │   ├── prompts.py          Reality + image prompt engineering
│   │   └── fallback.py         Safe reality if Gemini is unavailable
│   ├── requirements.txt
│   ├── settings.env            YOUR KEYS LIVE HERE (git-ignored)
│   ├── settings.example.env
└── frontend/
    ├── index.html              Landing + result dossier markup
    ├── styles.css              Cinematic visual system (haunted glowing logo)
    └── js/
        ├── api.js              The only place that calls the backend
        ├── narration.js        Splits the story into clean paragraphs
        ├── reality-view.js     Loading choreography + full dossier render
        └── app.js              Form + suggestion controller
```

## Run it (one click)

1. **Double-click `START-PARACOSM.command`** (in the `paracosm` folder).
   - First run sets up the Python environment and installs dependencies automatically (about a minute).
   - It then starts the server and opens the app in your browser for you.
   - If macOS says "unidentified developer" the first time: right-click the file -> **Open** -> **Open**. You only do this once.
   - Keep the Terminal window it opens **open** while you use the app. To stop, press Control-C or close that window.

2. That's it. A browser tab opens at the app automatically. Type a question, press the red arrow.

### Manual alternative (if you prefer the terminal)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
Then open `frontend/index.html`. Health check: http://localhost:8080/api/health


## Configuration (`backend/settings.env`)

Copy `settings.example.env` to `settings.env` and fill in:

| Key | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Story / reality generation |
| `GEMINI_MODEL` | Default `gemini-2.5-flash` |
| `POLLINATIONS_API_KEY` | Image generation |
| `POLLINATIONS_MODEL` | Default `flux` |
| `IMAGE_COUNT` | Number of images (default 3) |
| `POLLINATIONS_REQUEST_DELAY_SECONDS` | Politeness delay between image calls |

## ⚠️ Security

API keys are stored locally in `backend/settings.env`, which is excluded from Git through `.gitignore`.
Never commit or share your `settings.env` file. Use `settings.example.env` as the template and add your own API keys locally.
If an API key is ever accidentally committed or exposed publicly, rotate it immediately.

## Design notes

- **Haunted wordmark** — the PARACOSM logo breathes between bright and dim with irregular
  flickers and a red halo bloom, so it reads as an unstable, slightly eerie sign rather than a
  static title.
- **Staged loading** — the rift cycles through "Splitting the timeline → Mapping the divergence
  → Building consequences → Rendering alternate memories → Generating images" so the wait feels
  like a world being built.
- **Full dossier** — beyond the required title / summary / story / 3 images, the result shows a
  causal timeline, your alternate self, world changes, and long-term consequences.
- **Graceful failure** — unreachable backend and failed images produce clear messages, never
  silent black boxes.
- Respects `prefers-reduced-motion`.
