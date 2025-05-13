# Anysong.ai 🎵

AI harmonies extraction using Madmom, Librosa, Numpy (Python, flask) application that analyzes MP3 files to detect and display chord progressions in real-time. The app features a modern, responsive design with an animated musical note background and a sleek dark theme interface.

## Features ✨

- **Real-time Chord Detection**: Analyzes MP3 files and displays chord progressions as the music plays
- **Interactive Waveform Display**: Visual representation of the audio with playback controls
- **Responsive Design**: Optimized for both desktop and mobile devices
- **Dynamic Background**: Beautiful animated musical notes that create an immersive experience
- **Drag & Drop Support**: Easy file upload through drag and drop or file browser
- **Chord Timeline**: Visual representation of chord changes with timestamps
- **Transposition Support**: Ability to transpose chords to different keys
- **Mobile-Optimized Interface**: Full-screen mobile experience with native-like feel

## Technologies Used 🛠️

### Frontend
- **HTML5/CSS3**: Modern, semantic markup and styling
- **JavaScript (ES6+)**: Client-side functionality and animations
- **Bootstrap 5**: Responsive layout and UI components
- **Font Awesome 6**: Icons and visual elements
- **Google Fonts**: Custom typography (Quicksand)
- **Canvas API**: Background animation
- **Wavesurfer.js**: Audio waveform visualization
- **Web Audio API**: Audio processing and analysis

### Backend
- **Python**: Server-side processing
- **Flask**: Web framework
- **Librosa**: Audio analysis and chord detection
- **NumPy**: Numerical computations
- **SciPy**: Signal processing

### Features
- **CSS Custom Properties**: Dynamic theming
- **CSS Grid/Flexbox**: Modern layout system
- **Media Queries**: Responsive design
- **CSS Animations**: Smooth transitions and effects
- **HTML5 Drag & Drop API**: File upload functionality
- **Viewport Meta Tags**: Mobile optimization

## Getting Started 🚀

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage 📝

1. Upload an MP3 file by dragging and dropping or clicking the upload area
2. Click "Analyze" to process the audio file
3. Once analysis is complete, use the play button to start playback
4. Watch as chords are detected and displayed in real-time
5. Click on any chord in the timeline to jump to that position
6. Use the transpose controls to change the key if needed

## Browser Support 🌐

The application is optimized for modern browsers and supports:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Mobile Support 📱

The application is fully responsive and provides a native-like experience on mobile devices with:
- Full-screen mode
- Custom theme color for browser UI
- Optimized touch interactions
- Responsive layout adjustments
- Hide browser chrome on iOS

## Performance Optimizations ⚡

- Efficient canvas rendering
- Optimized audio processing
- Lazy loading of resources
- Smooth animations
- Minimal dependencies

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- WaveSurfer.js for audio visualization
- Librosa for audio analysis
- Bootstrap for UI components
- Font Awesome for icons
