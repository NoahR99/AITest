"""Core AI generation functionality for text-to-image, text-to-video, and image/video processing."""

import torch
from diffusers import (
    StableDiffusionPipeline, 
    StableDiffusionImg2ImgPipeline,
    DiffusionPipeline
)
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
import logging
from typing import Union, List, Optional, Tuple
from config import MODELS, DEFAULT_PARAMS, get_device, OUTPUT_DIR, DEVICE_CAPABILITIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIGenerator:
    """Main class for AI-powered image and video generation."""
    
    def __init__(self):
        self.device = get_device()
        self.capabilities = DEVICE_CAPABILITIES
        self.pipelines = {}
        logger.info(f"Initializing AI Generator on device: {self.device}")
        
        # Log device capabilities for debugging
        if self.device == "cuda":
            logger.info(f"CUDA device count: {torch.cuda.device_count()}")
            logger.info(f"CUDA device name: {torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else 'N/A'}")
        elif self.device == "mps":
            logger.info("Using Apple Metal Performance Shaders")
        else:
            logger.info("Using CPU (consider ARM-optimized builds for better performance)")
            import platform
            logger.info(f"Architecture: {platform.machine()}")
            logger.info(f"Processor: {platform.processor()}")
            
            # Log ARM-specific optimizations
            if self.capabilities.get("arm_optimized"):
                logger.info("ARM optimizations enabled")
                logger.info(f"Recommended image size: {self.capabilities['recommended_size']}x{self.capabilities['recommended_size']}")
                logger.info(f"Recommended inference steps: {self.capabilities['recommended_steps']}")
                logger.info(f"Memory limit: {self.capabilities['max_memory_gb']}GB")
    
    def _load_pipeline(self, pipeline_type: str, model_id: str = None) -> None:
        """Load a specific pipeline if not already loaded."""
        if pipeline_type in self.pipelines:
            return
            
        model_id = model_id or MODELS[pipeline_type]["default"]
        logger.info(f"Loading {pipeline_type} pipeline: {model_id}")
        
        try:
            # Determine optimal data type based on device capabilities
            if self.device == "cuda":
                torch_dtype = torch.float16
                variant = "fp16"
            elif self.device == "mps":
                torch_dtype = torch.float32  # MPS doesn't support float16 well
                variant = None
            else:  # CPU or other devices
                torch_dtype = getattr(torch, self.capabilities.get("dtype", "float32"))
                variant = None
            
            if pipeline_type == "text_to_image":
                pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch_dtype,
                    variant=variant,
                    safety_checker=None,
                    requires_safety_checker=False
                )
            elif pipeline_type == "image_to_image":
                pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch_dtype,
                    variant=variant,
                    safety_checker=None,
                    requires_safety_checker=False
                )
            elif pipeline_type == "text_to_video":
                pipeline = DiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch_dtype,
                    variant=variant
                )
            else:
                raise ValueError(f"Unknown pipeline type: {pipeline_type}")
            
            pipeline = pipeline.to(self.device)
            
            # Apply device-specific optimizations
            if self.device == "cuda":
                try:
                    # Try xformers first, but fall back to attention slicing if not available
                    try:
                        pipeline.enable_xformers_memory_efficient_attention()
                        logger.info("Enabled xformers memory efficient attention")
                    except (ImportError, AttributeError, Exception) as e:
                        logger.warning(f"xformers not available, using attention slicing instead: {e}")
                        pipeline.enable_attention_slicing()
                        logger.info("Enabled attention slicing as fallback")
                except Exception as e:
                    logger.warning(f"Could not enable memory optimizations: {e}")
            elif self.device == "mps":
                # MPS-specific optimizations - use attention slicing
                try:
                    pipeline.enable_attention_slicing()
                    logger.info("Enabled MPS-friendly attention slicing")
                except Exception as e:
                    logger.warning(f"Could not enable MPS optimizations: {e}")
            else:
                # CPU optimizations - always use attention slicing for better memory efficiency
                try:
                    pipeline.enable_attention_slicing()
                    logger.info("Enabled CPU-friendly attention slicing")
                except Exception as e:
                    logger.warning(f"Could not enable attention slicing: {e}")
                logger.info("Using CPU optimizations - consider setting OMP_NUM_THREADS for better performance")
            
            self.pipelines[pipeline_type] = pipeline
            logger.info(f"Successfully loaded {pipeline_type} pipeline")
            
        except Exception as e:
            logger.error(f"Failed to load {pipeline_type} pipeline: {e}")
            raise
    
    def generate_image_from_text(
        self, 
        prompt: str, 
        negative_prompt: str = None,
        width: int = None,
        height: int = None,
        num_inference_steps: int = None,
        guidance_scale: float = None,
        num_images: int = None,
        seed: int = None
    ) -> List[Image.Image]:
        """Generate images from text prompt."""
        self._load_pipeline("text_to_image")
        
        # Use default parameters if not specified
        params = DEFAULT_PARAMS["image"].copy()
        if width: params["width"] = width
        if height: params["height"] = height
        if num_inference_steps: params["num_inference_steps"] = num_inference_steps
        if guidance_scale: params["guidance_scale"] = guidance_scale
        if num_images: params["num_images"] = num_images
        
        generator = torch.Generator(device=self.device)
        if seed is not None:
            generator.manual_seed(seed)
        
        logger.info(f"Generating {params['num_images']} image(s) from text: '{prompt[:50]}...'")
        
        try:
            result = self.pipelines["text_to_image"](
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=params["width"],
                height=params["height"],
                num_inference_steps=params["num_inference_steps"],
                guidance_scale=params["guidance_scale"],
                num_images_per_prompt=params["num_images"],
                generator=generator
            )
            return result.images
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            raise
    
    def generate_image_from_image(
        self,
        prompt: str,
        init_image: Union[str, Path, Image.Image],
        strength: float = 0.75,
        negative_prompt: str = None,
        num_inference_steps: int = None,
        guidance_scale: float = None,
        seed: int = None
    ) -> List[Image.Image]:
        """Generate images from text prompt and initial image."""
        self._load_pipeline("image_to_image")
        
        # Load and prepare initial image
        if isinstance(init_image, (str, Path)):
            init_image = Image.open(init_image).convert("RGB")
        
        params = DEFAULT_PARAMS["image"].copy()
        if num_inference_steps: params["num_inference_steps"] = num_inference_steps
        if guidance_scale: params["guidance_scale"] = guidance_scale
        
        generator = torch.Generator(device=self.device)
        if seed is not None:
            generator.manual_seed(seed)
        
        logger.info(f"Generating image from image with prompt: '{prompt[:50]}...'")
        
        try:
            result = self.pipelines["image_to_image"](
                prompt=prompt,
                image=init_image,
                strength=strength,
                negative_prompt=negative_prompt,
                num_inference_steps=params["num_inference_steps"],
                guidance_scale=params["guidance_scale"],
                generator=generator
            )
            return result.images
        except Exception as e:
            logger.error(f"Failed to generate image from image: {e}")
            raise
    
    def generate_video_from_text(
        self,
        prompt: str,
        num_frames: int = None,
        width: int = None,
        height: int = None,
        num_inference_steps: int = None,
        guidance_scale: float = None,
        seed: int = None
    ) -> np.ndarray:
        """Generate video from text prompt."""
        self._load_pipeline("text_to_video")
        
        params = DEFAULT_PARAMS["video"].copy()
        if num_frames: params["num_frames"] = num_frames
        if width: params["width"] = width
        if height: params["height"] = height
        if num_inference_steps: params["num_inference_steps"] = num_inference_steps
        if guidance_scale: params["guidance_scale"] = guidance_scale
        
        generator = torch.Generator(device=self.device)
        if seed is not None:
            generator.manual_seed(seed)
        
        logger.info(f"Generating video from text: '{prompt[:50]}...'")
        
        try:
            result = self.pipelines["text_to_video"](
                prompt=prompt,
                num_frames=params["num_frames"],
                width=params["width"],
                height=params["height"],
                num_inference_steps=params["num_inference_steps"],
                guidance_scale=params["guidance_scale"],
                generator=generator
            )
            return result.frames[0]  # Returns numpy array of frames
        except Exception as e:
            logger.error(f"Failed to generate video: {e}")
            raise
    
    def save_images(self, images: List[Image.Image], prefix: str = "generated") -> List[Path]:
        """Save generated images to output directory."""
        saved_paths = []
        for i, image in enumerate(images):
            filename = f"{prefix}_{i+1:03d}.png"
            filepath = OUTPUT_DIR / filename
            image.save(filepath)
            saved_paths.append(filepath)
            logger.info(f"Saved image: {filepath}")
        return saved_paths
    
    def save_video(self, frames: np.ndarray, filename: str = "generated_video.mp4", fps: int = 8) -> Path:
        """Save generated video frames to output directory."""
        filepath = OUTPUT_DIR / filename
        
        # Get frame dimensions
        height, width = frames[0].shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(filepath), fourcc, fps, (width, height))
        
        # Write frames
        for frame in frames:
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)
        
        out.release()
        logger.info(f"Saved video: {filepath}")
        return filepath
    
    def cleanup(self):
        """Clean up GPU memory."""
        for pipeline in self.pipelines.values():
            del pipeline
        self.pipelines.clear()
        
        # Clear device-specific memory
        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("Cleaned up CUDA memory")
        elif self.device == "mps" and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            torch.mps.empty_cache()
            logger.info("Cleaned up MPS memory")
        else:
            logger.info("Cleaned up CPU memory")