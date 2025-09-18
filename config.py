"""Configuration settings for the AI generation app."""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.absolute()
OUTPUT_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Model configurations
MODELS = {
    "text_to_image": {
        "default": "runwayml/stable-diffusion-v1-5",
        "alternatives": [
            "stabilityai/stable-diffusion-2-1",
            "stabilityai/stable-diffusion-xl-base-1.0"
        ]
    },
    "text_to_video": {
        "default": "damo-vilab/text-to-video-ms-1.7b",
        "alternatives": []
    },
    "image_to_image": {
        "default": "runwayml/stable-diffusion-v1-5",
        "alternatives": []
    }
}

# Generation parameters
DEFAULT_PARAMS = {
    "image": {
        "width": 512,
        "height": 512,
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "num_images": 1
    },
    "video": {
        "width": 320,
        "height": 320,
        "num_frames": 16,
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }
}

# Device configuration
DEVICE = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"