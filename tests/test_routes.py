import io
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

def test_index_page(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200

def test_upload_no_file(client):
    """Test upload endpoint with no file."""
    response = client.post('/upload')
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_upload_empty_file(client):
    """Test upload endpoint with empty file selection."""
    response = client.post('/upload', data={'file': (io.BytesIO(b''), '')})
    assert response.status_code == 400
    assert b'No selected file' in response.data

def test_upload_invalid_extension(client):
    """Test upload endpoint with invalid file type."""
    data = {'file': (io.BytesIO(b'test data'), 'test.txt')}
    response = client.post('/upload', data=data)
    assert response.status_code == 400
    assert b'File type not allowed' in response.data

def test_upload_valid_file(client, app):
    """Test upload endpoint with valid MP3 file."""
    # Create a dummy MP3 file for testing
    test_data = b'dummy mp3 content'
    data = {'file': (io.BytesIO(test_data), 'test.mp3')}
    
    # Mock the process_audio_file function (since we're not using a real MP3)
    from unittest.mock import patch
    mock_result = {
        'status': 'success',
        'chord_sequence': [
            {'time': 0.0, 'chord': 'C'},
            {'time': 1.0, 'chord': 'G'}
        ]
    }
    
    with patch('app.routes.process_audio_file', return_value=mock_result):
        response = client.post('/upload', data=data)
        
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert len(response.json['chord_sequence']) == 2
    
    # Verify cleanup
    upload_dir = app.config['UPLOAD_FOLDER']
    assert len(os.listdir(upload_dir)) == 0  # Files should be cleaned up 

def test_youtube_search_no_query(client):
    response = client.get('/youtube/search')
    assert response.status_code == 400
    assert b'No search query provided' in response.data

def test_youtube_search_success(client):
    mock_results = {
        'entries': [
            {
                'id': 'video1',
                'title': 'Test Video 1',
                'thumbnail': 'http://example.com/thumb1.jpg',
                'duration': 180
            },
            {
                'id': 'video2',
                'title': 'Test Video 2',
                'thumbnail': 'http://example.com/thumb2.jpg',
                'duration': 240
            }
        ]
    }
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = mock_results
        
        response = client.get('/youtube/search?q=test query')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['items']) == 2
        assert data['items'][0]['id'] == 'video1'
        assert data['items'][1]['title'] == 'Test Video 2'

def test_youtube_search_error(client):
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = Exception('YouTube API error')
        
        response = client.get('/youtube/search?q=test')
        assert response.status_code == 500
        assert b'YouTube API error' in response.data

def test_youtube_process_no_video_id(client):
    response = client.post('/youtube/process', json={})
    assert response.status_code == 400
    assert b'No video ID provided' in response.data

def test_youtube_process_success(client, tmp_path):
    mock_info = {
        'title': 'Test YouTube Video',
        'duration': 180
    }
    
    mock_chord_sequence = [
        {'chord': '(0.0, 2.0, "C:maj")'},
        {'chord': '(2.0, 4.0, "G:maj")'}
    ]
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl, \
         patch('app.routes.process_audio_file') as mock_process:
        
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = mock_info
        mock_process.return_value = mock_chord_sequence
        
        response = client.post('/youtube/process', json={'video_id': 'test123'})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['title'] == 'Test YouTube Video'
        assert len(data['chord_sequence']) == 2
        assert data['chord_sequence'][0]['chord'] == '(0.0, 2.0, "C:maj")'

def test_youtube_process_download_error(client):
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = Exception('Download failed')
        
        response = client.post('/youtube/process', json={'video_id': 'test123'})
        assert response.status_code == 500
        assert b'Download failed' in response.data

def test_youtube_process_processing_error(client):
    mock_info = {'title': 'Test Video'}
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl, \
         patch('app.routes.process_audio_file') as mock_process:
        
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = mock_info
        mock_process.side_effect = Exception('Processing failed')
        
        response = client.post('/youtube/process', json={'video_id': 'test123'})
        assert response.status_code == 500
        assert b'Processing failed' in response.data 