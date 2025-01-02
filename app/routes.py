import os
from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from app.audio_processor import process_audio_file
import yt_dlp
import tempfile
from pathlib import Path

main = Blueprint('main', __name__)

# Create a directory for temporary YouTube audio files
YOUTUBE_TEMP_DIR = Path(tempfile.gettempdir()) / 'youtube_audio'
YOUTUBE_TEMP_DIR.mkdir(exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = current_app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # Process the audio file
        results = process_audio_file(filepath)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        # Return in the same format as youtube/process
        return jsonify({
            'status': 'success',
            'chord_sequence': results['chord_sequence']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/audio/<filename>')
def get_audio(filename):
    filepath = current_app.config['UPLOAD_FOLDER'] / secure_filename(filename)
    if not filepath.exists():
        return jsonify({'error': 'Audio file not found'}), 404
    
    return send_file(
        str(filepath),
        mimetype='audio/mpeg',
        as_attachment=False
    )

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = current_app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # Process the audio file
        results = process_audio_file(filepath)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@main.route('/youtube/search')
def youtube_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'match_filter': lambda info: None if float(info.get('duration', 0)) > 18 * 60 else info,  # Filter videos longer than 18 minutes
        'default_search': 'ytsearch5'  # Limit to 5 results
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f'ytsearch5:{query}', download=False)
            
            items = []
            for entry in results['entries']:
                if entry and float(entry.get('duration', 0)) <= 18 * 60:  # Double check duration
                    # Get the best quality thumbnail
                    thumbnail = None
                    if 'thumbnails' in entry:
                        thumbnails = entry['thumbnails']
                        # Try to get medium quality thumbnail first
                        thumbnail = next((t['url'] for t in thumbnails if t.get('id') == '2'), None)
                        if not thumbnail:
                            # Fallback to the first available thumbnail
                            thumbnail = thumbnails[0]['url'] if thumbnails else None
                    
                    items.append({
                        'id': entry['id'],
                        'title': entry['title'],
                        'thumbnail': thumbnail or f'https://i.ytimg.com/vi/{entry["id"]}/mqdefault.jpg',
                        'duration': str(entry.get('duration', 'Unknown'))
                    })
            
            return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/youtube/process', methods=['POST'])
def process_youtube():
    video_id = request.json.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video ID provided'}), 400

    # Create the audio file path
    audio_file = YOUTUBE_TEMP_DIR / f'{video_id}.mp3'

    try:
        if not audio_file.exists():
            # Download only if file doesn't exist
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': str(YOUTUBE_TEMP_DIR / video_id),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id, download=True)

        # Process the audio file
        results = process_audio_file(str(audio_file))
        
        return jsonify({
            'status': 'success',
            'chord_sequence': results.get('chord_sequence', []),
            'title': info.get('title', 'YouTube Video') if 'info' in locals() else 'YouTube Video'
        })
            
    except Exception as e:
        # Clean up the file if there was an error
        if audio_file.exists():
            audio_file.unlink()
        return jsonify({'error': str(e)}), 500

@main.route('/youtube/audio/<video_id>')
def get_youtube_audio(video_id):
    audio_file = YOUTUBE_TEMP_DIR / f'{video_id}.mp3'
    if not audio_file.exists():
        return jsonify({'error': 'Audio file not found'}), 404
    
    return send_file(
        str(audio_file),
        mimetype='audio/mpeg',
        as_attachment=False
    ) 