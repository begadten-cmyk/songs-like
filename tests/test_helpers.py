import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import _simplify_track


def test_simplify_track_complete():
    """Test _simplify_track with complete track data."""
    track = {
        'id': 'track123',
        'name': 'Test Song',
        'artists': [
            {'name': 'Artist One'},
            {'name': 'Artist Two'}
        ],
        'album': {
            'name': 'Test Album',
            'images': [
                {'url': 'https://example.com/large.jpg'},
                {'url': 'https://example.com/medium.jpg'},
                {'url': 'https://example.com/small.jpg'}
            ]
        },
        'preview_url': 'https://example.com/preview.mp3',
        'external_urls': {
            'spotify': 'https://spotify.com/track/track123'
        }
    }
    
    result = _simplify_track(track)
    
    assert result['id'] == 'track123'
    assert result['name'] == 'Test Song'
    assert result['artists'] == 'Artist One, Artist Two'
    assert result['album'] == 'Test Album'
    assert result['image'] == 'https://example.com/medium.jpg'
    assert result['preview_url'] == 'https://example.com/preview.mp3'
    assert result['external_url'] == 'https://spotify.com/track/track123'


def test_simplify_track_missing_fields():
    """Test _simplify_track with missing optional fields."""
    track = {
        'id': 'track456',
        'name': 'Minimal Song'
    }
    
    result = _simplify_track(track)
    
    assert result['id'] == 'track456'
    assert result['name'] == 'Minimal Song'
    assert result['artists'] == ''
    assert result['album'] is None
    assert result['image'] is None
    assert result['preview_url'] is None
    assert result['external_url'] is None


def test_simplify_track_single_image():
    """Test _simplify_track with only one image."""
    track = {
        'id': 'track789',
        'name': 'One Image Song',
        'artists': [{'name': 'Solo Artist'}],
        'album': {
            'name': 'Solo Album',
            'images': [
                {'url': 'https://example.com/only.jpg'}
            ]
        },
        'external_urls': {'spotify': 'https://spotify.com/track/track789'}
    }
    
    result = _simplify_track(track)
    
    assert result['image'] == 'https://example.com/only.jpg'
    assert result['artists'] == 'Solo Artist'


def test_simplify_track_no_images():
    """Test _simplify_track with no images."""
    track = {
        'id': 'track000',
        'name': 'No Image Song',
        'artists': [{'name': 'Artist'}],
        'album': {
            'name': 'Album',
            'images': []
        },
        'external_urls': {'spotify': 'https://spotify.com/track/track000'}
    }
    
    result = _simplify_track(track)
    
    assert result['image'] is None
