let searchTimeout = null;
let currentQuery = '';

const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');
const searchLoading = document.getElementById('searchLoading');
const recommendationsSection = document.getElementById('recommendationsSection');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const recommendationsLoading = document.getElementById('recommendationsLoading');
const errorMessage = document.getElementById('errorMessage');

searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    if (query.length === 0) {
        hideDropdown();
        return;
    }
    
    searchLoading.classList.remove('hidden');
    
    searchTimeout = setTimeout(() => {
        performSearch(query);
    }, 300);
});

searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const firstSelectBtn = searchDropdown.querySelector('.select-btn');
        if (firstSelectBtn) {
            firstSelectBtn.click();
        }
    } else if (e.key === 'Escape') {
        hideDropdown();
    }
});

document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        hideDropdown();
    }
});

async function performSearch(query) {
    currentQuery = query;
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`Search failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (currentQuery !== query) {
            return;
        }
        
        displaySearchResults(data.items || []);
    } catch (error) {
        console.error('Search error:', error);
        searchDropdown.innerHTML = '<div class="error-message">Search failed. Please try again.</div>';
        searchDropdown.classList.remove('hidden');
    } finally {
        searchLoading.classList.add('hidden');
    }
}

function displaySearchResults(tracks) {
    if (tracks.length === 0) {
        searchDropdown.innerHTML = '<div class="error-message">No results found.</div>';
        searchDropdown.classList.remove('hidden');
        return;
    }
    
    searchDropdown.innerHTML = tracks.map(track => `
        <div class="dropdown-item">
            <div class="track-info">
                <div class="track-name">${escapeHtml(track.name)}</div>
                <div class="track-artist">${escapeHtml(track.artists)}</div>
            </div>
            <button class="select-btn" onclick="selectTrack('${track.id}')">Select</button>
        </div>
    `).join('');
    
    searchDropdown.classList.remove('hidden');
}

function hideDropdown() {
    searchDropdown.classList.add('hidden');
    searchLoading.classList.add('hidden');
}

async function selectTrack(trackId) {
    hideDropdown();
    searchInput.value = '';
    
    recommendationsSection.classList.remove('hidden');
    recommendationsGrid.innerHTML = '';
    errorMessage.classList.add('hidden');
    recommendationsLoading.classList.remove('hidden');
    
    try {
        const response = await fetch(`/api/recommendations?track_id=${trackId}`);
        
        if (!response.ok) {
            throw new Error(`Recommendations failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayRecommendations(data.items || []);
    } catch (error) {
        console.error('Recommendations error:', error);
        errorMessage.textContent = `Could not fetch recommendations. Try again.`;
        errorMessage.classList.remove('hidden');
    } finally {
        recommendationsLoading.classList.add('hidden');
    }
}

function displayRecommendations(tracks) {
    if (tracks.length === 0) {
        errorMessage.textContent = 'No similar songs found. Try another track.';
        errorMessage.classList.remove('hidden');
        return;
    }
    
    recommendationsGrid.innerHTML = tracks.map(track => createSongCard(track)).join('');
}

function createSongCard(track) {
    const imageHtml = track.image 
        ? `<img src="${escapeHtml(track.image)}" alt="${escapeHtml(track.name)}" class="song-image">`
        : `<div class="placeholder-image">No Image</div>`;
    
    const featuresHtml = track.features ? `
        <div class="song-features">
            <span class="feature-chip">Tempo: ${track.features.tempo} BPM</span>
            <span class="feature-chip">Energy: ${track.features.energy}</span>
            <span class="feature-chip">Valence: ${track.features.valence}</span>
            <span class="feature-chip">Dance: ${track.features.danceability}</span>
        </div>
    ` : '';
    
    const previewHtml = track.preview_url ? `
        <audio controls class="preview-audio">
            <source src="${escapeHtml(track.preview_url)}" type="audio/mpeg">
            Your browser does not support audio playback.
        </audio>
    ` : '';
    
    return `
        <div class="song-card">
            ${imageHtml}
            <div class="song-title">${escapeHtml(track.name)}</div>
            <div class="song-artist">${escapeHtml(track.artists)}</div>
            ${featuresHtml}
            <div class="song-actions">
                <a href="${escapeHtml(track.external_url)}" target="_blank" class="spotify-link">
                    Open in Spotify
                </a>
                ${previewHtml}
            </div>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}
