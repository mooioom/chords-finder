import numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
import logging

def process_audio_file(file_path):
    """
    Process an audio file to detect chords using Madmom.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        dict: Dictionary containing chord progression and timing information
    """
    try:
        # Create processing pipeline
        chord_processor = SequentialProcessor([
            DeepChromaProcessor(),
            DeepChromaChordRecognitionProcessor()
        ])
        
        # Process the audio file
        chord_sequence = chord_processor(str(file_path))
        
        # Debug logging
        logging.debug(f"Chord sequence type: {type(chord_sequence)}")
        logging.debug(f"Chord sequence shape: {chord_sequence.shape if hasattr(chord_sequence, 'shape') else 'no shape'}")
        logging.debug(f"Chord sequence content: {chord_sequence}")

        # Format results
        results = []
        if hasattr(chord_sequence, 'shape'):
            # Handle numpy array format
            for i in range(len(chord_sequence)):
                results.append({
                    'time': float(i * 0.5),  # Assuming 0.5 second intervals
                    'chord': str(chord_sequence[i])
                })
        else:
            # Handle list format
            for entry in chord_sequence:
                results.append({
                    'time': float(entry[0]) if len(entry) > 0 else 0.0,
                    'chord': str(entry[1]) if len(entry) > 1 else 'N'
                })

        return {
            'status': 'success',
            'chord_sequence': results
        }
        
    except Exception as e:
        logging.error(f"Error processing audio file: {str(e)}")
        raise Exception(f"Error processing audio file: {str(e)}") 