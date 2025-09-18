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
from config import MODELS, DEFAULT_PARAMS, DEVICE, OUTPUT_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIGenerator:
    """Main class for AI-powered image and video generation."""
    
    def __init__(self):
        self.device = DEVICE
        self.pipelines = {}
        logger.info(f"Initializing AI Generator on device: {self.device}")
    
    def _load_pipeline(self, pipeline_type: str, model_id: str = None) -> None:
        """Load a specific pipeline if not already loaded."""
        if pipeline_type in self.pipelines:
            return
            
        model_id = model_id or MODELS[pipeline_type]["default"]
        logger.info(f"Loading {pipeline_type} pipeline: {model_id}")
        
        try:
            if pipeline_type == "text_to_image":
                pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False
                )
            elif pipeline_type == "image_to_image":
                pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False
                )
            elif pipeline_type == "text_to_video":
                pipeline = DiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    variant="fp16" if self.device == "cuda" else None
                )
            else:
                raise ValueError(f"Unknown pipeline type: {pipeline_type}")
            
            pipeline = pipeline.to(self.device)
            if self.device == "cuda":
                pipeline.enable_xformers_memory_efficient_attention()
            
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
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("Cleaned up GPU memory")