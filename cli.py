#!/usr/bin/env python3
"""Command-line interface for the AI generation app."""

import argparse
import sys
from pathlib import Path
from typing import Optional
import logging
from ai_generator import AIGenerator
from config import OUTPUT_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="AI-powered image and video generation")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Text-to-image command
    img_parser = subparsers.add_parser('text-to-image', help='Generate images from text')
    img_parser.add_argument('prompt', type=str, help='Text prompt for image generation')
    img_parser.add_argument('--negative-prompt', type=str, help='Negative prompt')
    img_parser.add_argument('--width', type=int, default=512, help='Image width')
    img_parser.add_argument('--height', type=int, default=512, help='Image height')
    img_parser.add_argument('--steps', type=int, default=20, help='Number of inference steps')
    img_parser.add_argument('--guidance', type=float, default=7.5, help='Guidance scale')
    img_parser.add_argument('--num-images', type=int, default=1, help='Number of images to generate')
    img_parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    img_parser.add_argument('--output-prefix', type=str, default='text2img', help='Output filename prefix')
    
    # Image-to-image command
    img2img_parser = subparsers.add_parser('image-to-image', help='Generate images from text and initial image')
    img2img_parser.add_argument('prompt', type=str, help='Text prompt for image generation')
    img2img_parser.add_argument('input_image', type=str, help='Path to input image')
    img2img_parser.add_argument('--negative-prompt', type=str, help='Negative prompt')
    img2img_parser.add_argument('--strength', type=float, default=0.75, help='Transformation strength (0-1)')
    img2img_parser.add_argument('--steps', type=int, default=20, help='Number of inference steps')
    img2img_parser.add_argument('--guidance', type=float, default=7.5, help='Guidance scale')
    img2img_parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    img2img_parser.add_argument('--output-prefix', type=str, default='img2img', help='Output filename prefix')
    
    # Text-to-video command
    vid_parser = subparsers.add_parser('text-to-video', help='Generate videos from text')
    vid_parser.add_argument('prompt', type=str, help='Text prompt for video generation')
    vid_parser.add_argument('--frames', type=int, default=16, help='Number of video frames')
    vid_parser.add_argument('--width', type=int, default=320, help='Video width')
    vid_parser.add_argument('--height', type=int, default=320, help='Video height')
    vid_parser.add_argument('--steps', type=int, default=20, help='Number of inference steps')
    vid_parser.add_argument('--guidance', type=float, default=7.5, help='Guidance scale')
    vid_parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    vid_parser.add_argument('--fps', type=int, default=8, help='Video frame rate')
    vid_parser.add_argument('--output-name', type=str, default='text2video.mp4', help='Output video filename')
    
    # List outputs command
    list_parser = subparsers.add_parser('list-outputs', help='List generated files')
    
    # Clear outputs command
    clear_parser = subparsers.add_parser('clear-outputs', help='Clear all generated files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'text-to-image':
            generate_text_to_image(args)
        elif args.command == 'image-to-image':
            generate_image_to_image(args)
        elif args.command == 'text-to-video':
            generate_text_to_video(args)
        elif args.command == 'list-outputs':
            list_outputs()
        elif args.command == 'clear-outputs':
            clear_outputs()
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        sys.exit(1)


def generate_text_to_image(args):
    """Generate images from text prompt."""
    logger.info("Starting text-to-image generation...")
    
    generator = AIGenerator()
    try:
        images = generator.generate_image_from_text(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            num_images=args.num_images,
            seed=args.seed
        )
        
        saved_paths = generator.save_images(images, args.output_prefix)
        
        print(f"\n✅ Successfully generated {len(images)} image(s):")
        for path in saved_paths:
            print(f"   📁 {path}")
            
    finally:
        generator.cleanup()


def generate_image_to_image(args):
    """Generate images from text prompt and initial image."""
    logger.info("Starting image-to-image generation...")
    
    # Check if input image exists
    input_path = Path(args.input_image)
    if not input_path.exists():
        logger.error(f"Input image not found: {input_path}")
        sys.exit(1)
    
    generator = AIGenerator()
    try:
        images = generator.generate_image_from_image(
            prompt=args.prompt,
            init_image=input_path,
            strength=args.strength,
            negative_prompt=args.negative_prompt,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            seed=args.seed
        )
        
        saved_paths = generator.save_images(images, args.output_prefix)
        
        print(f"\n✅ Successfully generated {len(images)} image(s):")
        for path in saved_paths:
            print(f"   📁 {path}")
            
    finally:
        generator.cleanup()


def generate_text_to_video(args):
    """Generate video from text prompt."""
    logger.info("Starting text-to-video generation...")
    
    generator = AIGenerator()
    try:
        frames = generator.generate_video_from_text(
            prompt=args.prompt,
            num_frames=args.frames,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            seed=args.seed
        )
        
        saved_path = generator.save_video(frames, args.output_name, args.fps)
        
        print(f"\n✅ Successfully generated video:")
        print(f"   📁 {saved_path}")
        print(f"   📊 {len(frames)} frames at {args.fps} FPS")
            
    finally:
        generator.cleanup()


def list_outputs():
    """List all generated files."""
    files = list(OUTPUT_DIR.glob("*"))
    if not files:
        print("No generated files found.")
        return
    
    print(f"\n📂 Generated files in {OUTPUT_DIR}:")
    for file in sorted(files):
        if file.is_file():
            size = file.stat().st_size
            size_str = format_file_size(size)
            print(f"   📄 {file.name} ({size_str})")


def clear_outputs():
    """Clear all generated files."""
    files = list(OUTPUT_DIR.glob("*"))
    if not files:
        print("No files to clear.")
        return
    
    count = 0
    for file in files:
        if file.is_file():
            file.unlink()
            count += 1
    
    print(f"✅ Cleared {count} file(s) from {OUTPUT_DIR}")


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    main()