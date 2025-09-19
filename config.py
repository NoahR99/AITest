"""Configuration settings for the AI generation app."""

import os
from pathlib import Path
from device_utils import detect_device_capabilities, get_optimized_model_params, setup_performance_environment

# Setup performance environment early
setup_performance_environment()

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

# Device configuration
def get_device():
    """Detect the best available device for AI processing."""
    try:
        import torch
    except ImportError:
        # If torch is not available, default to CPU
        return "cpu"
    
    # Check if CUDA is explicitly disabled via environment variables
    if (os.environ.get("CUDA_VISIBLE_DEVICES") == "" or 
        os.environ.get("FORCE_CPU", "").lower() in ("1", "true", "yes")):
        return "cpu"
    
    # Check for CUDA availability (NVIDIA GPUs)
    try:
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        # CUDA might be broken or not properly installed, fall back to CPU
        pass
    
    # Check for Metal Performance Shaders (Apple Silicon)
    try:
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        # MPS might be broken, fall back to CPU
        pass
    
    # Fallback to CPU for all other cases (including ARM processors)
    return "cpu"

# Detect device capabilities and get optimized parameters
DEVICE_CAPABILITIES = detect_device_capabilities()
DEFAULT_PARAMS = get_optimized_model_params(DEVICE_CAPABILITIES)

# Lazy device detection - only called when needed
DEVICE = None