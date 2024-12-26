import io
import os
import pytest
from pathlib import Path

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