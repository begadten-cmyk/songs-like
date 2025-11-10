import os
import time
import logging
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

token_cache = {
    'access_token': None,
    'expires_at': 0
}


def get_spotify_token():
    """Get Spotify access token using Client Credentials flow with caching."""
    now = time.time()
    
    if token_cache['access_token'] and now < (token_cache['expires_at'] - 30):
        return token_cache['access_token']
    
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise ValueError("Spotify credentials not configured")
    
    logger.debug("Fetching new Spotify access token")
    
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(
            auth_url,
            auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
            data=auth_data,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        token_cache['access_token'] = data['access_token']
        token_cache['expires_at'] = now + data['expires_in']
        
        logger.debug(f"Token acquired, expires in {data['expires_in']}s")
        return token_cache['access_token']
        
    except Exception as e:
        logger.error(f"Failed to get Spotify token: {e}")
        raise


def sp_get(path, params=None):
    """Make authenticated GET request to Spotify API."""
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1{path}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Spotify API error for {path}: {e}")
        raise


def _simplify_track(track):
    """Convert Spotify track object to simplified format."""
    artists = ', '.join([artist['name'] for artist in track.get('artists', [])])
    album = track.get('album', {})
    images = album.get('images', [])
    
    image = None
    if len(images) >= 2:
        image = images[1]['url']
    elif len(images) >= 1:
        image = images[0]['url']
    
    return {
        'id': track.get('id'),
        'name': track.get('name'),
        'artists': artists,
        'album': album.get('name'),
        'image': image,
        'preview_url': track.get('preview_url'),
        'external_url': track.get('external_urls', {}).get('spotify')
    }


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'ok': True})


@app.route('/')
def index():
    """Render main application page."""
    return render_template('index.html')


@app.route('/api/search')
def search():
    """Search for tracks on Spotify."""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'items': []})
    
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return jsonify({'error': 'Spotify credentials not configured'}), 500
    
    try:
        results = sp_get('/search', params={
            'q': query,
            'type': 'track',
            'market': 'US',
            'limit': 10
        })
        
        tracks = results.get('tracks', {}).get('items', [])
        simplified = [_simplify_track(track) for track in tracks]
        
        return jsonify({'items': simplified})
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({'error': 'Search failed'}), 500


@app.route('/api/recommendations')
def recommendations():
    """Get song recommendations with fallback to related artists."""
    track_id = request.args.get('track_id', '')
    
    if not track_id:
        return jsonify({'error': 'track_id required'}), 400
    
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return jsonify({'error': 'Spotify credentials not configured'}), 500
    
    recommendations = []
    
    try:
        logger.debug(f"Trying /recommendations for track {track_id}")
        results = sp_get('/recommendations', params={
            'seed_tracks': track_id,
            'limit': 12,
            'market': 'US'
        })
        
        recommendations = results.get('tracks', [])
        
        if recommendations:
            logger.debug(f"Got {len(recommendations)} recommendations from /recommendations")
        
    except Exception as e:
        logger.debug(f"Recommendations endpoint failed: {e}, trying fallback")
    
    if not recommendations:
        logger.debug("Using fallback: search-based recommendations")
        try:
            track_data = sp_get(f'/tracks/{track_id}')
            artists = track_data.get('artists', [])
            album = track_data.get('album', {})
            track_name = track_data.get('name', '')
            
            if not artists:
                return jsonify({'items': []})
            
            artist_name = artists[0]['name']
            artist_id = artists[0]['id']
            
            all_tracks = []
            
            try:
                artist_info = sp_get(f'/artists/{artist_id}')
                genres = artist_info.get('genres', [])[:2]
                
                for genre in genres:
                    try:
                        search_results = sp_get('/search', params={
                            'q': f'genre:{genre}',
                            'type': 'track',
                            'market': 'US',
                            'limit': 20
                        })
                        genre_tracks = search_results.get('tracks', {}).get('items', [])
                        all_tracks.extend(genre_tracks)
                    except Exception as e:
                        logger.debug(f"Genre search failed for {genre}: {e}")
            except Exception as e:
                logger.debug(f"Failed to get artist genres: {e}")
            
            try:
                search_results = sp_get('/search', params={
                    'q': f'artist:{artist_name}',
                    'type': 'track',
                    'market': 'US',
                    'limit': 30
                })
                artist_tracks = search_results.get('tracks', {}).get('items', [])
                all_tracks.extend(artist_tracks)
            except Exception as e:
                logger.debug(f"Artist search failed: {e}")
            
            words = track_name.split()[:3]
            for word in words:
                if len(word) > 3:
                    try:
                        search_results = sp_get('/search', params={
                            'q': word,
                            'type': 'track',
                            'market': 'US',
                            'limit': 15
                        })
                        keyword_tracks = search_results.get('tracks', {}).get('items', [])
                        all_tracks.extend(keyword_tracks)
                    except Exception as e:
                        logger.debug(f"Keyword search failed for {word}: {e}")
            
            seen_ids = {track_id}
            unique_tracks = []
            for track in all_tracks:
                if track and track.get('id') and track['id'] not in seen_ids:
                    unique_tracks.append(track)
                    seen_ids.add(track['id'])
                if len(unique_tracks) >= 12:
                    break
            
            recommendations = unique_tracks[:12]
            logger.debug(f"Fallback returned {len(recommendations)} tracks")
            
        except Exception as e:
            logger.error(f"Fallback also failed: {e}")
            return jsonify({'items': []})
    
    simplified = [_simplify_track(track) for track in recommendations]
    
    track_ids = [t['id'] for t in simplified if t['id']]
    features_map = {}
    
    if track_ids:
        try:
            for i in range(0, len(track_ids), 100):
                chunk = track_ids[i:i+100]
                ids_param = ','.join(chunk)
                features_data = sp_get('/audio-features', params={'ids': ids_param})
                
                for feature in features_data.get('audio_features', []):
                    if feature:
                        features_map[feature['id']] = {
                            'tempo': round(feature.get('tempo', 0)),
                            'energy': round(feature.get('energy', 0), 2),
                            'valence': round(feature.get('valence', 0), 2),
                            'danceability': round(feature.get('danceability', 0), 2)
                        }
        except Exception as e:
            logger.debug(f"Audio features fetch failed (403/429 expected): {e}")
    
    for track in simplified:
        if track['id'] in features_map:
            track['features'] = features_map[track['id']]
    
    return jsonify({'items': simplified})


if __name__ == '__main__':
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("\n" + "="*60)
        print("WARNING: Spotify credentials not found!")
        print("Please add these secrets in Replit:")
        print("  - SPOTIFY_CLIENT_ID")
        print("  - SPOTIFY_CLIENT_SECRET")
        print("="*60 + "\n")
    
    print(f"\n🎵 SongsLike starting on http://{HOST}:{PORT}")
    print(f"Preview will be available in Replit webview\n")
    
    app.run(host=HOST, port=PORT, debug=False)
