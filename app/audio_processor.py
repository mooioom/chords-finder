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
        last_chord = None
        last_time = 0.0
        first_chord = True

        if isinstance(chord_sequence, np.ndarray):
            # Handle numpy array format
            for i, chord in enumerate(chord_sequence):
                time = float(i) / 10.0  # Assuming 10 fps
                
                if first_chord:
                    last_chord = chord
                    last_time = time
                    first_chord = False
                    continue
                
                if chord != last_chord:
                    results.append({
                        'time': last_time,
                        'chord': f"({last_time}, {time}, '{last_chord}')"
                    })
                    last_chord = chord
                    last_time = time

            # Add the final chord
            if last_chord:
                final_time = float(len(chord_sequence)) / 10.0
                results.append({
                    'time': last_time,
                    'chord': f"({last_time}, {final_time}, '{last_chord}')"
                })
        else:
            # Handle list format
            for entry in chord_sequence:
                try:
                    if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                        time = float(entry[0])
                        chord = str(entry[1])
                    else:
                        continue

                    if first_chord:
                        last_chord = chord
                        last_time = time
                        first_chord = False
                        continue
                    
                    if chord != last_chord:
                        results.append({
                            'time': last_time,
                            'chord': f"({last_time}, {time}, '{last_chord}')"
                        })
                        last_chord = chord
                        last_time = time
                except (IndexError, ValueError) as e:
                    logging.warning(f"Skipping malformed entry {entry}: {str(e)}")
                    continue

            # Add the final chord
            if last_chord and len(chord_sequence) > 0:
                try:
                    final_time = float(chord_sequence[-1][0]) if isinstance(chord_sequence[-1], (list, tuple)) else len(chord_sequence)
                    results.append({
                        'time': last_time,
                        'chord': f"({last_time}, {final_time}, '{last_chord}')"
                    })
                except (IndexError, ValueError) as e:
                    logging.warning(f"Error processing final chord: {str(e)}")

        return {
            'status': 'success',
            'chord_sequence': results
        }
        
    except Exception as e:
        logging.error(f"Error processing audio file: {str(e)}")
        raise Exception(f"Error processing audio file: {str(e)}") 