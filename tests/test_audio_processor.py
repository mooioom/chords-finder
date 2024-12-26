import pytest
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.audio_processor import process_audio_file
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def test_ffmpeg_installation():
    """Test that ffmpeg is installed and accessible."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        assert result.returncode == 0
        assert 'ffmpeg version' in result.stdout
    except FileNotFoundError:
        pytest.fail("ffmpeg is not installed or not in PATH")

def test_audio_file_conversion():
    """Test that ffmpeg can convert a simple audio file."""
    # Create a silent audio file using ffmpeg
    test_file = Path('tests/test_uploads/test_silence.mp3')
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate 1 second of silence
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', 
            '-t', '1', '-q:a', '9', '-acodec', 'libmp3lame',
            str(test_file)
        ], capture_output=True, check=True)
        
        assert test_file.exists()
        assert test_file.stat().st_size > 0
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
        if test_file.parent.exists():
            test_file.parent.rmdir()

def test_audio_file_processing_with_ffmpeg():
    """Test that our audio processor can work with ffmpeg to process MP3 files."""
    # Create a test audio file with a specific frequency
    test_file = Path('tests/test_uploads/test_tone.mp3')
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate a 1-second 440Hz tone (A4 note)
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', 
            '-i', 'sine=frequency=440:duration=1',
            '-q:a', '9', '-acodec', 'libmp3lame',
            str(test_file)
        ], capture_output=True, check=True)
        
        # Process the file
        result = process_audio_file(test_file)
        
        # Verify the result
        assert result['status'] == 'success'
        assert len(result['chord_sequence']) > 0
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
        if test_file.parent.exists():
            test_file.parent.rmdir()

def test_process_audio_file_success():
    """Test successful audio processing."""
    # Mock the Madmom processors
    mock_chord_sequence = [
        (0.0, "C"),
        (1.0, "G"),
        (2.0, "Am"),
        (3.0, "F")
    ]
    
    with patch('app.audio_processor.SequentialProcessor') as mock_processor:
        # Configure the mock
        instance = mock_processor.return_value
        instance.return_value = mock_chord_sequence
        
        # Test the function
        result = process_audio_file(Path('dummy.mp3'))
        
        assert result['status'] == 'success'
        assert len(result['chord_sequence']) == 4
        assert result['chord_sequence'][0]['time'] == 0.0
        assert result['chord_sequence'][0]['chord'] == 'C'

def test_process_audio_file_error():
    """Test error handling in audio processing."""
    with patch('app.audio_processor.SequentialProcessor') as mock_processor:
        # Configure the mock to raise an exception
        instance = mock_processor.return_value
        instance.side_effect = Exception("Audio processing failed")
        
        # Test the function
        with pytest.raises(Exception) as exc_info:
            process_audio_file(Path('dummy.mp3'))
        
        assert "Error processing audio file" in str(exc_info.value)

def test_process_audio_file_invalid_path():
    """Test processing with invalid file path."""
    with pytest.raises(Exception) as exc_info:
        process_audio_file(Path('nonexistent.mp3'))
    
    assert "Error processing audio file" in str(exc_info.value) 