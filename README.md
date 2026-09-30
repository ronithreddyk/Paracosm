# PARACOSM — Alternate Reality Simulator

Ask one impossible question. PARACOSM opens a doorway into another version of reality —
a named world, a cinematic 300–500 word narration, a causal timeline, your alternate self,
and three AI-generated photographs of a life that never happened.

```
What if Messi became a cricketer?
What if Earth had two moons?
What if I moved to Tokyo?
```

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

## ⚠️ Security note

`settings.env` in this folder currently contains **live API keys**. It is listed in
`.gitignore` so it won't be committed — but if these keys were ever shared, pasted, or pushed
anywhere public, **rotate them** (issue new keys and delete the old ones). Keep real keys only
in `settings.env`; keep `settings.example.env` blank.

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
