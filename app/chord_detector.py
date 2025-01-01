from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor

def detect_chords(audio_file):
    # Create a more comprehensive chord detection processor
    # This includes major, minor, dominant 7th, major 7th, minor 7th, diminished
    chord_processor = DeepChromaChordRecognitionProcessor(
        models=['majmin', 'maj7', 'min7', '7', 'dim'],  # Include more chord types
        fps=20  # Increased from 10 to 20 for more precise timing
    )
    
    # Create the processing pipeline
    processor = SequentialProcessor([
        DeepChromaProcessor(),  # Extract deep chroma features
        chord_processor  # Detect chords with extended vocabulary
    ])
    
    # Process the audio file
    chords = processor(audio_file)
    
    # Filter and format the results
    formatted_chords = []
    last_chord = None
    
    for frame in chords:
        # Each frame contains [time, chord_label]
        if len(frame) != 2:
            continue
            
        time, chord_label = frame
        
        # Skip if it's the same chord as the last one
        if last_chord and last_chord[2] == chord_label:
            last_chord[1] = time  # Update end time
            continue
        
        # If we have a previous chord, add it to the list
        if last_chord:
            formatted_chords.append(tuple(last_chord))
        
        # Start tracking the new chord
        last_chord = [time, time, chord_label]
    
    # Add the last chord if exists
    if last_chord:
        formatted_chords.append(tuple(last_chord))
    
    return formatted_chords 