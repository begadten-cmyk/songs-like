**Live demo:** https://songs-like.onrender.com

# SongsLike

A fast web app to find songs that feel the same using the Spotify Web API.

## Features
- Live search as you type
- 12 similar songs with cover art and preview links
- Fallback if Spotify recs fail (uses artist/genre/keyword search)
- Optional chips: tempo, energy, valence, danceability
- No login (client credentials only)

## Run Locally
1) Make a Spotify app at https://developer.spotify.com/dashboard to get:
   - SPOTIFY_CLIENT_ID
   - SPOTIFY_CLIENT_SECRET
2) In your terminal:
```bash
pip install -r requirements.txt
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
python app.py
