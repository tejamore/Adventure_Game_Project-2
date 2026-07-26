# Quest for the Legendary Treasure — Web Adventure Game

A browser-playable, text-adventure treasure hunt built with **Python** and
**Flask**, converted from the original CLI `adventure_game.py` script into a
deployable web application. Built and refined with **GitHub Copilot** in VS
Code.

## Features
- Enter your name to begin the quest
- Explore a **dark forest** or a **mysterious cave**
- Multiple branching decision points (river/tree, torch/darkness, etc.)
- Win by finding the treasure, lose by making a poor decision
- Restart the adventure at any time
- Session-based state (each visitor has their own independent playthrough)

## Project structure
```
adventure_game_app/
├── app.py                 # Flask application & game logic
├── templates/
│   ├── base.html           # Shared layout
│   ├── start.html          # Name entry / intro screen
│   ├── scene.html          # Story + choice screen
│   └── result.html         # Win / lose screen
├── static/
│   └── style.css           # Adventure-themed styling
├── requirements.txt
├── render.yaml              # Render Blueprint (auto-deploy config)
├── Procfile                 # Alternate start command reference
└── .gitignore
```

## Requirements
- Python 3.9+
- pip
- (Optional) Git + a GitHub account, for deploying to Render

Python packages (see `requirements.txt`):
- `Flask==3.0.3`
- `gunicorn==22.0.0` (production WSGI server used on Render)

## 1. Run locally

```bash
# 1. Clone or download this project, then move into the folder
cd adventure_game_app

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## 2. Push the project to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Flask adventure game"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 3. Deploy to Render

**Option A — One-click Blueprint (uses `render.yaml`):**
1. Log in to [render.com](https://render.com) and click **New +** → **Blueprint**.
2. Connect your GitHub account and select the repository you just pushed.
3. Render reads `render.yaml` automatically and provisions a **Web Service**
   with the correct build/start commands and a generated `SECRET_KEY`.
4. Click **Apply** — Render will build and deploy automatically.

**Option B — Manual Web Service setup:**
1. Log in to [render.com](https://render.com) and click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Under **Environment Variables**, add:
   - `SECRET_KEY` → any random string (used to sign Flask session cookies)
5. Click **Create Web Service**. Render installs dependencies and starts the
   app automatically. Every future push to `main` triggers an auto-deploy.

Once deployed, Render gives you a public URL such as:
`https://adventure-game.onrender.com`

## 4. Environment variables

| Variable     | Required | Purpose                                   |
|--------------|----------|--------------------------------------------|
| `SECRET_KEY` | Recommended | Signs Flask session cookies (game state) |
| `PORT`       | Auto-set by Render | Port the app listens on          |

If `SECRET_KEY` is not set, the app falls back to a development default —
fine for local testing, but you should set a real value in production.

## 5. How the game maps to the original CLI project

| Original CLI task                     | Web app equivalent                              |
|----------------------------------------|--------------------------------------------------|
| `start_game()` asks for player's name  | `/` and `/start` routes, `start.html` form        |
| Initial choice: forest or cave         | `/scene/choice` route                              |
| `forest_path()` with river/tree choice | `/scene/forest`, `forest_river`, `forest_tree`     |
| `cave_path()` with torch/dark choice   | `/scene/cave`, `cave_torch`, `cave_dark`           |
| Win / lose endings                     | `result.html`, `SCENES[...]["result"]`             |
| Restart option                         | `/restart` route, "Play Again" button              |

## Troubleshooting
- **Blank page / 500 error on Render:** check the Render **Logs** tab; most
  often caused by a missing dependency (re-check `requirements.txt`) or a
  missing `SECRET_KEY`.
- **Session/game state resets unexpectedly:** make sure cookies are enabled
  in your browser; the game relies on Flask's signed session cookie.
- **Port already in use locally:** stop other apps using port 5000, or run
  `PORT=5050 python app.py`.
