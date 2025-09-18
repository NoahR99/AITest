#!/usr/bin/env python3
"""
Example script demonstrating how to use the AI Generator programmatically.
This script shows basic usage of the AIGenerator class.
"""

from ai_generator import AIGenerator
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run example AI generation tasks."""
    print("🤖 AI Generator Example Script")
    print("=" * 40)
    
    # Initialize the AI generator
    generator = AIGenerator()
    
    try:
        # Example 1: Generate an image from text
        print("\n📸 Example 1: Text to Image")
        print("Generating image from text prompt...")
        
        prompt = "A serene mountain lake at sunset, digital art"
        images = generator.generate_image_from_text(
            prompt=prompt,
            negative_prompt="blurry, low quality",
            width=512,
            height=512,
            num_inference_steps=20,
            guidance_scale=7.5,
            seed=42  # For reproducible results
        )
        
        # Save the generated images
        saved_paths = generator.save_images(images, "example_text2img")
        print(f"✅ Generated {len(images)} image(s):")
        for path in saved_paths:
            print(f"   📁 {path}")
        
        # Example 2: Create a simple video (if available)
        print("\n🎬 Example 2: Text to Video")
        print("Generating video from text prompt...")
        
        try:
            video_prompt = "A butterfly flying in a garden"
            frames = generator.generate_video_from_text(
                prompt=video_prompt,
                num_frames=16,
                width=320,
                height=320,
                num_inference_steps=15,  # Fewer steps for faster generation
                seed=123
            )
            
            # Save the video
            video_path = generator.save_video(frames, "example_text2video.mp4", fps=8)
            print(f"✅ Generated video:")
            print(f"   📁 {video_path}")
            print(f"   📊 {len(frames)} frames")
            
        except Exception as e:
            print(f"⚠️  Video generation skipped: {e}")
            print("   (Video models may not be available)")
        
        print("\n🎉 Examples completed successfully!")
        print(f"   Check the 'outputs' folder for generated files.")
        
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    finally:
        # Clean up GPU memory
        generator.cleanup()
        print("\n🧹 Cleaned up resources.")


if __name__ == "__main__":
    main()