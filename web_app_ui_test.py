"""Simple web interface for UI testing without AI dependencies."""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
import logging

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure app from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'ai-generator-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # Default 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create output directory for testing
OUTPUT_DIR = Path('outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with generation options."""
    return render_template('index.html')

@app.route('/text-to-image', methods=['GET', 'POST'])
def text_to_image():
    """Text-to-image generation page."""
    if request.method == 'POST':
        flash('Image generation would happen here!', 'success')
        return render_template('text_to_image.html', images=[])
    return render_template('text_to_image.html')

@app.route('/image-to-image', methods=['GET', 'POST'])
def image_to_image():
    """Image-to-image generation page."""
    if request.method == 'POST':
        flash('Image transformation would happen here!', 'success')
        return render_template('image_to_image.html', images=[])
    return render_template('image_to_image.html')

@app.route('/text-to-video', methods=['GET', 'POST'])
def text_to_video():
    """Text-to-video generation page."""
    if request.method == 'POST':
        flash('Video generation would happen here!', 'success')
        return render_template('text_to_video.html', video=None)
    return render_template('text_to_video.html')

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    """Serve generated files."""
    return send_file(OUTPUT_DIR / filename)

@app.route('/gallery')
def gallery():
    """Gallery page showing all generated files."""
    files = []
    for file_path in OUTPUT_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                'name': file_path.name,
                'path': str(file_path.relative_to(OUTPUT_DIR)),
                'type': 'video' if file_path.suffix.lower() in ['.mp4', '.avi', '.mov'] else 'image'
            })
    
    files.sort(key=lambda x: x['name'], reverse=True)
    return render_template('gallery.html', files=files)

if __name__ == '__main__':
    import os
    
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"🚀 Starting AI Generator Web App (UI Test Mode)")
    print(f"🌐 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    app.run(debug=debug, host=host, port=port)