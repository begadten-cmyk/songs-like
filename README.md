**Live demo:** https://songs-like.onrender.com

# SongsLike

Find songs that *feel the same* using the Spotify Web API.

## Features
- **Live search** as you type
- **12 similar songs** with cover art, artist, and preview links
- **Fallback** if Spotify `/recommendations` is limited (uses artist/genre/keyword search)
- **Optional audio chips**: tempo, energy, valence, danceability (shown only when available)
- **No login** needed (Client Credentials flow)

## Quick Start (Local)
1) Create a Spotify app at <https://developer.spotify.com/dashboard>  
   Get:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`

2) In your terminal:
```bash
pip install -r requirements.txt
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
python app.py

pp runs at http://127.0.0.1:8080.

Deploy on Render

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app --bind 0.0.0.0:$PORT

Env Vars: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

API

GET /health → health check

GET / → web UI

GET /api/search?q=<query> → Spotify track search

GET /api/recommendations?track_id=<id> → similar tracks

Tech

Backend: Python 3 + Flask, Gunicorn

Frontend: HTML, CSS, vanilla JS

API: Spotify Web API (Client Credentials OAuth)

How it picks “similar”

Try Spotify /recommendations with the selected track as a seed.

If blocked/limited, fall back to search mixes: same artist, related genres, and keyword matches.

Project Structure
.
├── app.py               # Flask app + endpoints
├── requirements.txt     # Python deps (Flask, requests, python-dotenv, gunicorn)
├── templates/
│   └── index.html       # UI
├── static/
│   ├── styles.css
│   └── app.js
└── tests/               # Basic smoke tests

Notes

If /audio-features returns 403/429 or missing data, the UI hides those chips and still shows results.

Rate limits or missing preview URLs are handled gracefully in the UI.
