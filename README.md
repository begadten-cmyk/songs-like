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

