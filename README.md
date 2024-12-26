# 🎵 Chords Finder

A web application that analyzes MP3 files and detects the chord progression (ffmpeg, madmom, flask)! 🎸

## ✨ Features

- 🎼 Upload any MP3 file and get instant chord analysis
- 🎹 Real-time chord display during playback
- 📊 Visual waveform representation
- ⏱️ Time-synchronized chord highlighting
- 🎯 Accurate chord detection using deep learning

## 🚀 Getting Started

### Prerequisites

- 🐳 Docker and Docker Compose
- 🖥️ Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chords-finder.git
cd chords-finder
```

2. Build and start the Docker containers:
```bash
docker-compose up --build
```

⚠️ **Note**: The initial build might take 5-10 minutes as it needs to install ffmpeg and other dependencies. This is normal! ffmpeg is a large but essential package for audio processing.

3. Once the build is complete, visit:
```
http://localhost:5020
```

## 🎯 How to Use

1. 📂 Click the upload button and select an MP3 file
2. ⚡ Wait for the analysis to complete (this might take a few seconds depending on the file size)
3. ▶️ Hit the Play button to start playback
4. 🎵 Watch as the chords are highlighted in real-time!

## 🛠️ Technical Stack

- 🐍 Python/Flask for the backend server
- 🎼 Madmom for deep learning-based chord detection
- 🔊 FFmpeg for audio processing and conversion
- 🌊 Wavesurfer.js for audio visualization
- 🎨 Bootstrap & Font Awesome for the UI
- 🐳 Docker for containerization

## 📝 Notes

- The application uses deep learning models for chord detection, so the first analysis might take a few seconds
- Supported file format: MP3
- For best results, use high-quality audio files with clear instrumentation
- The chord detection works best with:
  - 🎸 Guitar-based music
  - 🎹 Piano pieces
  - 🎵 Clear harmonic content

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Madmom library for the amazing audio processing capabilities
- FFmpeg for reliable audio handling
- All the open-source contributors who make this possible!

## ⚠️ Troubleshooting

If you encounter any issues:

1. Make sure Docker is running and has enough resources allocated
2. For audio processing issues, ensure ffmpeg is properly installed in the container
3. If the analysis takes too long, try with a smaller file first
4. Check the browser console for any JavaScript errors

Created by Eldad Levi using Cursor-AI (anthropic)
Licened MIT fork it, upgrade and give some music to the world 🎸
