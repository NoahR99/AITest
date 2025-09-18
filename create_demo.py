#!/usr/bin/env python3
"""
Demo script that creates sample output files to demonstrate the application structure
without requiring actual AI model downloads.
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import random
import time

# Create output directories
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def create_demo_image(text: str, filename: str, width: int = 512, height: int = 512):
    """Create a demo image with text overlay."""
    # Create a colorful gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        r = int(255 * (y / height))
        g = int(128 + 127 * np.sin(2 * np.pi * y / height))
        b = int(255 - 255 * (y / height))
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add some noise/texture
    for _ in range(1000):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        brightness = random.randint(-30, 30)
        pixel = img.getpixel((x, y))
        new_pixel = tuple(max(0, min(255, c + brightness)) for c in pixel)
        img.putpixel((x, y), new_pixel)
    
    # Add text overlay
    try:
        # Try to use a default font, fall back to default if not available
        font = ImageFont.load_default()
    except:
        font = None
    
    # Add semi-transparent overlay for text
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 128))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Calculate text position
    text_lines = [
        "🤖 AI GENERATOR DEMO",
        f"Prompt: {text[:30]}{'...' if len(text) > 30 else ''}",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "This is a demo image created",
        "without actual AI models."
    ]
    
    y_offset = height // 2 - len(text_lines) * 15
    for line in text_lines:
        bbox = overlay_draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        overlay_draw.text((x, y_offset), line, fill=(255, 255, 255, 255), font=font)
        y_offset += 30
    
    # Composite the overlay
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Save the image
    filepath = OUTPUT_DIR / filename
    img.save(filepath)
    print(f"✅ Created demo image: {filepath}")
    return filepath

def create_demo_video(text: str, filename: str, width: int = 320, height: int = 320, fps: int = 8, duration: int = 2):
    """Create a demo video with animated text."""
    filepath = OUTPUT_DIR / filename
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(filepath), fourcc, fps, (width, height))
    
    total_frames = fps * duration
    
    for frame_num in range(total_frames):
        # Create a frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animated background
        t = frame_num / total_frames
        for y in range(height):
            for x in range(width):
                r = int(128 + 127 * np.sin(2 * np.pi * (x + frame_num * 2) / width))
                g = int(128 + 127 * np.cos(2 * np.pi * (y + frame_num * 3) / height))
                b = int(128 + 127 * np.sin(2 * np.pi * t * 4))
                frame[y, x] = [b, g, r]  # BGR for OpenCV
        
        # Add text overlay
        text_lines = [
            "AI VIDEO DEMO",
            f"Frame {frame_num + 1}/{total_frames}",
            f"Prompt: {text[:20]}{'...' if len(text) > 20 else ''}",
        ]
        
        for i, line in enumerate(text_lines):
            y_pos = 50 + i * 30
            cv2.putText(frame, line, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        out.write(frame)
    
    out.release()
    print(f"✅ Created demo video: {filepath} ({total_frames} frames)")
    return filepath

def main():
    """Create demo files."""
    print("🎬 Creating AI Generator Demo Files")
    print("=" * 40)
    
    # Create demo images
    prompts = [
        "A beautiful sunset over mountains",
        "A robot in a cyberpunk city",
        "A cat wearing a wizard hat",
        "Ocean waves at the beach"
    ]
    
    print("\n📸 Creating demo images...")
    for i, prompt in enumerate(prompts):
        filename = f"demo_text2img_{i+1:03d}.png"
        create_demo_image(prompt, filename)
    
    # Create demo video
    print("\n🎬 Creating demo video...")
    create_demo_video("A bird flying through clouds", "demo_text2video.mp4")
    
    print(f"\n🎉 Demo files created in '{OUTPUT_DIR}' directory!")
    print("\nThese demo files show what the application structure looks like.")
    print("To generate real AI content, install the requirements and run:")
    print("  python cli.py text-to-image 'your prompt here'")
    print("  python web_app.py")

if __name__ == "__main__":
    main()