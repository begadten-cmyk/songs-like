# SongsLike

## Overview

SongsLike is a web application that helps users discover similar songs using Spotify's Web API. Users can search for a song, select it from live search results, and instantly receive 12 personalized song recommendations with album artwork, artist information, and audio preview capabilities. The application is designed as a fast, production-ready MVP that requires no user authentication and uses Spotify's Client Credentials OAuth flow for API access.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Choice**: Vanilla HTML/CSS/JavaScript with no build step
- **Rationale**: Minimizes complexity and deployment overhead for an MVP; enables instant page loads without bundling
- **Key Components**:
  - Single-page application (SPA) pattern with client-side rendering
  - Debounced search input (300ms delay) to reduce API calls
  - Dropdown component for live search results
  - Grid layout for displaying song recommendations
  - Loading states and error handling for better UX

**UI/UX Decisions**:
- Dark theme optimized for music discovery (`#0f1115` background)
- Responsive grid layout that adapts to different screen sizes
- Keyboard navigation support (Enter to select, Escape to close)
- Click-outside-to-close pattern for dropdown

### Backend Architecture

**Framework**: Flask 3.0.3 (Python 3.11)
- **Rationale**: Lightweight, minimal boilerplate, perfect for small APIs with templating needs
- **Key Features**:
  - Template rendering for the main page
  - RESTful API endpoints for search and recommendations
  - Server-side token management and caching

**Authentication & Token Management**:
- Uses Spotify Client Credentials flow (no user login required)
- Token caching mechanism to minimize OAuth requests:
  - Stores `access_token` and `expires_at` in memory
  - Auto-refreshes 30 seconds before expiration
  - Reduces latency and API rate limit concerns

**API Design Pattern**:
- Helper function `sp_get(path, params)` centralizes Spotify API calls
- Consistent error handling with status code validation
- 10-second timeout on all external requests
- Base URL prefixing for cleaner endpoint definitions

### Fallback & Resilience Strategy

**Problem**: Spotify's `/recommendations` endpoint may fail or be unavailable for certain API credentials
**Solution**: Multi-tiered fallback approach
1. Primary: Use Spotify's native recommendations API
2. Fallback: Search-based recommendations using:
   - Genre-based searches
   - Artist-specific top tracks
   - Keyword/style searches

**Pros**:
- Guarantees results even when recommendations API is restricted
- Maintains user experience consistency
- No dead-ends or error states

**Cons**:
- Fallback results may be less accurate than native recommendations
- Requires additional API calls (managed within rate limits)

### Data Transformation

**Track Simplification**: All Spotify track objects are normalized via `_simplify_track()` helper
- Extracts only necessary fields (id, name, artists, album, image, preview_url, external_url)
- Handles missing fields gracefully with defaults
- Reduces payload size for frontend
- Artists array flattened to comma-separated string for easier display

**Audio Features (Optional)**:
- Tempo, energy, valence, danceability chips
- Only displayed when successfully fetched from `/audio-features` endpoint
- Gracefully hidden if endpoint access is denied (common for some API credentials)
- Non-blocking: recommendations still load if audio features fail

## External Dependencies

### Third-Party APIs

**Spotify Web API** (primary integration)
- **Authentication**: OAuth 2.0 Client Credentials flow
- **Endpoints Used**:
  - `POST /api/token` - OAuth token retrieval
  - `GET /v1/search` - Song search (type=track, market=US, limit=10)
  - `GET /v1/recommendations` - Get similar songs (primary method)
  - `GET /v1/audio-features/{id}` - Optional audio characteristics
  - Fallback endpoints for search-based recommendations (genre, artist searches)
- **Rate Limiting**: Managed through token caching and request throttling
- **Base URL**: `https://api.spotify.com/v1`
- **Timeout**: 10 seconds per request

### Environment Configuration

**Required Secrets** (stored in Replit Secrets):
- `SPOTIFY_CLIENT_ID` - Spotify Developer App Client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify Developer App Client Secret

**Optional Environment Variables**:
- `HOST` - Server host (default: `0.0.0.0`)
- `PORT` - Server port (default: `5000`, Replit typically uses `8080`)

### Python Dependencies

- **Flask 3.0.3** - Web framework for routing and templating
- **requests 2.32.3** - HTTP library for Spotify API communication
- **python-dotenv 1.0.1** - Environment variable management (.env file support)
- **pytest 8.0.0** - Testing framework for unit tests

### Deployment Platform

**Replit-Specific Configuration**:
- `.replit` file configures run command: `python app.py`
- `replit.nix` specifies Python 3.11 runtime environment
- Secrets management through Replit's encrypted storage
- Automatic HTTPS and domain provisioning