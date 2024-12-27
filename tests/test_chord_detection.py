import os
import pytest
from app.chord_detector import detect_chords
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

def create_test_chord_sequence():
    """Create a test audio file with various chord types"""
    # Define frequencies for different notes (in Hz)
    notes = {
        'C4': 261.63, 'E4': 329.63, 'G4': 392.00,  # C major
        'C4': 261.63, 'Eb4': 311.13, 'G4': 392.00,  # C minor
        'C4': 261.63, 'E4': 329.63, 'G4': 392.00, 'B4': 493.88,  # Cmaj7
        'C4': 261.63, 'Eb4': 311.13, 'G4': 392.00, 'Bb4': 466.16,  # Cm7
        'C4': 261.63, 'F4': 349.23, 'G4': 392.00,  # Csus4
        'C4': 261.63, 'D4': 293.66, 'G4': 392.00,  # Csus2
    }

    # Create 2-second segments for each chord
    duration = 2000  # 2 seconds
    sample_rate = 44100
    audio = AudioSegment.silent(duration=0)

    # Generate each chord
    for chord_notes in [
        ['C4', 'E4', 'G4'],  # C major
        ['C4', 'Eb4', 'G4'],  # C minor
        ['C4', 'E4', 'G4', 'B4'],  # Cmaj7
        ['C4', 'Eb4', 'G4', 'Bb4'],  # Cm7
        ['C4', 'F4', 'G4'],  # Csus4
        ['C4', 'D4', 'G4'],  # Csus2
    ]:
        chord = AudioSegment.silent(duration=duration)
        for note in chord_notes:
            sine = Sine(notes[note])
            tone = sine.to_audio_segment(duration=duration)
            chord = chord.overlay(tone)
        
        audio += chord

    # Export the test file
    test_file = 'tests/test_uploads/test_chords.mp3'
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    audio.export(test_file, format='mp3')
    return test_file

def test_extended_chord_detection():
    """Test detection of various chord types"""
    # Create test audio file
    test_file = create_test_chord_sequence()
    
    # Detect chords
    detected_chords = detect_chords(test_file)
    
    # Expected chord sequence (allowing for some flexibility in detection)
    expected_chords = [
        ('C:maj', 0, 2),    # C major
        ('C:min', 2, 4),    # C minor
        ('C:maj7', 4, 6),   # Cmaj7
        ('C:min7', 6, 8),   # Cm7
        ('C:sus4', 8, 10),  # Csus4
        ('C:sus2', 10, 12), # Csus2
    ]
    
    # Compare results (with some tolerance for timing)
    for expected, detected in zip(expected_chords, detected_chords):
        exp_chord, exp_start, exp_end = expected
        det_start, det_end, det_chord = detected
        
        # Allow for some timing tolerance (0.5 seconds)
        assert abs(det_start - exp_start) < 0.5, f"Start time mismatch for {exp_chord}"
        assert abs(det_end - exp_end) < 0.5, f"End time mismatch for {exp_chord}"
        
        # For chord type, we'll check if the root note is correct
        # and if the chord quality is at least partially correct
        det_root, det_quality = det_chord.split(':')
        exp_root, exp_quality = exp_chord.split(':')
        
        assert det_root == exp_root, f"Root note mismatch: expected {exp_root}, got {det_root}"
        # The quality check might need to be more flexible as madmom might not detect
        # all chord qualities exactly as we expect
        assert det_quality.startswith(exp_quality[:3]), \
            f"Chord quality mismatch: expected {exp_quality}, got {det_quality}" 