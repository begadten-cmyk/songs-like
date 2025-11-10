# SongsLike

A fast, production-ready web app that helps you discover similar songs using Spotify's API.

## Features

- **Live Search**: Type a song name and get instant search results from Spotify
- **Smart Recommendations**: Get 12 similar songs with cover art, artist info, and preview buttons
- **Fallback Logic**: If Spotify's recommendations API fails, the app automatically falls back to related artists' top tracks
- **Audio Features**: Optional tempo, energy, valence, and danceability chips (shown only when available)
- **No Login Required**: Uses Spotify Client Credentials flow (no user authentication needed)

## How to Run on Replit

1. **Add Spotify API Credentials**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create an app to get your Client ID and Client Secret
   - In Replit, open the **Secrets** tool (🔒 icon in sidebar)
   - Add these two secrets:
     - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID
     - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret

2. **Run the App**:
   - The app will start automatically when you open this Repl
   - Or click the "Run" button at the top
   - The preview will open showing the SongsLike interface

3. **Try It Out**:
   - Type a song name in the search box (e.g., "Nonstop")
   - Click "Select" on a search result
   - View 12 similar song recommendations with cover art and preview buttons

## Tech Stack

- **Backend**: Python 3.11 + Flask
- **Frontend**: Vanilla HTML/CSS/JavaScript (no build step)
- **API**: Spotify Web API with Client Credentials OAuth flow

## Notes

- **Audio Features**: The optional feature chips (tempo, energy, valence, danceability) require Spotify API access to the audio-features endpoint. If your app doesn't have access or the API returns 403/429, the app will gracefully hide these chips and still show all song recommendations.
- **Fallback Strategy**: If Spotify's `/recommendations` endpoint fails, the app automatically falls back to fetching related artists' top tracks, ensuring you always get results.

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /` - Main application page
- `GET /api/search?q=<query>` - Search for songs
- `GET /api/recommendations?track_id=<id>` - Get similar songs

## Testing

Run unit tests with:
```bash
pytest tests/
```
