"""Simple web interface for the AI generation app using Flask."""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
import logging
from ai_generator import AIGenerator
from config import OUTPUT_DIR, TEMP_DIR
import threading
import time

app = Flask(__name__)
app.secret_key = 'ai-generator-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global generator instance (initialized lazily)
generator = None


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_generator():
    """Get or create the AI generator instance."""
    global generator
    if generator is None:
        generator = AIGenerator()
    return generator


@app.route('/')
def index():
    """Main page with generation options."""
    return render_template('index.html')


@app.route('/text-to-image', methods=['GET', 'POST'])
def text_to_image():
    """Text-to-image generation page."""
    if request.method == 'POST':
        try:
            prompt = request.form.get('prompt', '').strip()
            if not prompt:
                flash('Please enter a prompt', 'error')
                return redirect(url_for('text_to_image'))
            
            # Get parameters
            negative_prompt = request.form.get('negative_prompt', '').strip() or None
            width = int(request.form.get('width', 512))
            height = int(request.form.get('height', 512))
            steps = int(request.form.get('steps', 20))
            guidance = float(request.form.get('guidance', 7.5))
            num_images = int(request.form.get('num_images', 1))
            seed = request.form.get('seed')
            seed = int(seed) if seed and seed.strip() else None
            
            # Generate images
            gen = get_generator()
            images = gen.generate_image_from_text(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance,
                num_images=num_images,
                seed=seed
            )
            
            # Save images
            saved_paths = gen.save_images(images, "web_text2img")
            
            # Get relative paths for web display
            web_paths = [str(path.relative_to(OUTPUT_DIR)) for path in saved_paths]
            
            flash(f'Successfully generated {len(images)} image(s)!', 'success')
            return render_template('text_to_image.html', images=web_paths, prompt=prompt)
            
        except Exception as e:
            logger.error(f"Error in text-to-image: {e}")
            flash(f'Error generating image: {str(e)}', 'error')
    
    return render_template('text_to_image.html')


@app.route('/image-to-image', methods=['GET', 'POST'])
def image_to_image():
    """Image-to-image generation page."""
    if request.method == 'POST':
        try:
            prompt = request.form.get('prompt', '').strip()
            if not prompt:
                flash('Please enter a prompt', 'error')
                return redirect(url_for('image_to_image'))
            
            # Check for uploaded file
            if 'input_image' not in request.files:
                flash('Please upload an input image', 'error')
                return redirect(url_for('image_to_image'))
            
            file = request.files['input_image']
            if file.filename == '':
                flash('Please select an input image', 'error')
                return redirect(url_for('image_to_image'))
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload an image.', 'error')
                return redirect(url_for('image_to_image'))
            
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            temp_path = TEMP_DIR / f"input_{int(time.time())}_{filename}"
            file.save(temp_path)
            
            # Get parameters
            negative_prompt = request.form.get('negative_prompt', '').strip() or None
            strength = float(request.form.get('strength', 0.75))
            steps = int(request.form.get('steps', 20))
            guidance = float(request.form.get('guidance', 7.5))
            seed = request.form.get('seed')
            seed = int(seed) if seed and seed.strip() else None
            
            # Generate images
            gen = get_generator()
            images = gen.generate_image_from_image(
                prompt=prompt,
                init_image=temp_path,
                strength=strength,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance,
                seed=seed
            )
            
            # Save images
            saved_paths = gen.save_images(images, "web_img2img")
            
            # Clean up temp file
            temp_path.unlink()
            
            # Get relative paths for web display
            web_paths = [str(path.relative_to(OUTPUT_DIR)) for path in saved_paths]
            
            flash(f'Successfully generated {len(images)} image(s)!', 'success')
            return render_template('image_to_image.html', images=web_paths, prompt=prompt)
            
        except Exception as e:
            logger.error(f"Error in image-to-image: {e}")
            flash(f'Error generating image: {str(e)}', 'error')
            # Clean up temp file if it exists
            if 'temp_path' in locals() and temp_path.exists():
                temp_path.unlink()
    
    return render_template('image_to_image.html')


@app.route('/text-to-video', methods=['GET', 'POST'])
def text_to_video():
    """Text-to-video generation page."""
    if request.method == 'POST':
        try:
            prompt = request.form.get('prompt', '').strip()
            if not prompt:
                flash('Please enter a prompt', 'error')
                return redirect(url_for('text_to_video'))
            
            # Get parameters
            frames = int(request.form.get('frames', 16))
            width = int(request.form.get('width', 320))
            height = int(request.form.get('height', 320))
            steps = int(request.form.get('steps', 20))
            guidance = float(request.form.get('guidance', 7.5))
            fps = int(request.form.get('fps', 8))
            seed = request.form.get('seed')
            seed = int(seed) if seed and seed.strip() else None
            
            # Generate video
            gen = get_generator()
            video_frames = gen.generate_video_from_text(
                prompt=prompt,
                num_frames=frames,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance,
                seed=seed
            )
            
            # Save video
            video_filename = f"web_text2video_{int(time.time())}.mp4"
            saved_path = gen.save_video(video_frames, video_filename, fps)
            
            # Get relative path for web display
            web_path = str(saved_path.relative_to(OUTPUT_DIR))
            
            flash('Successfully generated video!', 'success')
            return render_template('text_to_video.html', video=web_path, prompt=prompt)
            
        except Exception as e:
            logger.error(f"Error in text-to-video: {e}")
            flash(f'Error generating video: {str(e)}', 'error')
    
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
    app.run(debug=True, host='0.0.0.0', port=5000)