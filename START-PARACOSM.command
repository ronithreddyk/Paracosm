#!/bin/zsh
# ===== PARACOSM one-click launcher =====
# Double-click this file. First run sets everything up; later runs just start.

HERE="$(cd "$(dirname "$0")" && pwd)"

# Clear the macOS "downloaded file" flag that causes "Operation not permitted"
xattr -dr com.apple.quarantine "$HERE" 2>/dev/null

cd "$HERE/backend" || { echo "Could not find the backend folder."; exit 1; }

echo "==============================================="
echo "  PARACOSM is starting up"
echo "==============================================="

if [ ! -d ".venv" ]; then
  echo "First-time setup: building the environment (about a minute)..."
  python3 -m venv .venv || { echo "Setup failed while creating the environment."; exit 1; }
fi

source .venv/bin/activate || { echo "Could not activate the environment."; exit 1; }

echo "Checking dependencies..."
python3 -m pip install --quiet --upgrade pip >/dev/null 2>&1
python3 -m pip install --quiet -r requirements.txt || { echo "Setup failed while installing dependencies."; exit 1; }

( sleep 3; open "$HERE/frontend/index.html" ) &

echo ""
echo "  PARACOSM is running at http://localhost:8080"
echo "  Your browser will open automatically."
echo "  KEEP THIS WINDOW OPEN while using the app."
echo "  To stop: press Control-C, or just close this window."
echo ""

python3 main.py
