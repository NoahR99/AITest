"""Device detection and optimization utilities for different platforms."""

import os
import platform
import logging

logger = logging.getLogger(__name__)


def detect_device_capabilities():
    """Detect device capabilities and return optimization settings."""
    capabilities = {
        "device": "cpu",
        "dtype": "float32",
        "memory_optimization": True,
        "max_memory_gb": 8,
        "recommended_steps": 20,
        "recommended_size": 512
    }
    
    # Detect architecture
    machine = platform.machine().lower()
    processor = platform.processor().lower()
    is_arm = any(arch in machine for arch in ['arm', 'aarch64']) or 'arm' in processor
    
    logger.info(f"Detected architecture: {machine}")
    logger.info(f"Processor: {processor}")
    
    if is_arm:
        logger.info("ARM processor detected - optimizing for ARM performance")
        capabilities.update({
            "memory_optimization": True,
            "max_memory_gb": 6,  # Conservative for ARM systems
            "recommended_steps": 15,  # Fewer steps for faster generation
            "recommended_size": 512,  # Smaller default size
            "arm_optimized": True
        })
    
    # Try to import torch to check device support
    try:
        import torch
        
        if torch.cuda.is_available() and not is_arm:
            capabilities["device"] = "cuda"
            capabilities["dtype"] = "float16"
            capabilities["max_memory_gb"] = torch.cuda.get_device_properties(0).total_memory // (1024**3)
            logger.info(f"CUDA available with {capabilities['max_memory_gb']}GB VRAM")
        
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            capabilities["device"] = "mps"
            capabilities["dtype"] = "float32"  # MPS works better with float32
            logger.info("MPS (Apple Silicon) available")
        
        else:
            logger.info("Using CPU device")
            # Set OMP threads for better CPU performance
            if is_arm:
                # ARM systems often have many cores but lower per-core performance
                cpu_count = os.cpu_count() or 4
                omp_threads = min(cpu_count, 8)  # Cap at 8 threads
                os.environ.setdefault("OMP_NUM_THREADS", str(omp_threads))
                logger.info(f"Set OMP_NUM_THREADS to {omp_threads} for ARM optimization")
    
    except ImportError:
        logger.warning("PyTorch not available, using default CPU settings")
    
    return capabilities


def get_optimized_model_params(capabilities):
    """Get model parameters optimized for the detected device."""
    base_params = {
        "image": {
            "width": capabilities["recommended_size"],
            "height": capabilities["recommended_size"],
            "num_inference_steps": capabilities["recommended_steps"],
            "guidance_scale": 7.5,
            "num_images": 1
        },
        "video": {
            "width": min(320, capabilities["recommended_size"]),
            "height": min(320, capabilities["recommended_size"]),
            "num_frames": 12 if capabilities.get("arm_optimized") else 16,
            "num_inference_steps": max(10, capabilities["recommended_steps"] - 5),
            "guidance_scale": 7.5
        }
    }
    
    # Adjust for low-memory systems
    if capabilities["max_memory_gb"] < 8:
        base_params["image"]["width"] = 512
        base_params["image"]["height"] = 512
        base_params["image"]["num_inference_steps"] = 10
        base_params["video"]["num_frames"] = 8
        logger.info("Reduced parameters for low-memory system")
    
    return base_params


def setup_performance_environment():
    """Set up environment variables for optimal performance."""
    # Set reasonable defaults for various performance settings
    env_vars = {
        "TOKENIZERS_PARALLELISM": "false",  # Avoid tokenizer warnings
        "TRANSFORMERS_CACHE": os.path.join(os.getcwd(), "cache", "transformers"),
        "HF_HOME": os.path.join(os.getcwd(), "cache", "huggingface"),
    }
    
    # Check if user wants to force CPU mode
    if os.environ.get("FORCE_CPU", "").lower() in ("1", "true", "yes"):
        env_vars["CUDA_VISIBLE_DEVICES"] = ""
        logger.info("FORCE_CPU enabled - disabling CUDA")
    
    # ARM-specific optimizations
    machine = platform.machine().lower()
    if any(arch in machine for arch in ['arm', 'aarch64']):
        env_vars.update({
            "MKL_NUM_THREADS": "1",  # Disable Intel MKL on ARM
            "NUMEXPR_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "4",  # OpenBLAS is more common on ARM
        })
    else:
        # x86/x64 CPU optimizations
        cpu_count = os.cpu_count() or 4
        omp_threads = min(cpu_count, 8)  # Cap at 8 threads for stability
        env_vars.update({
            "OMP_NUM_THREADS": str(omp_threads),
        })
    
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
            logger.info(f"Set {key}={value}")
    
    # Create cache directories
    for cache_dir in [env_vars.get("TRANSFORMERS_CACHE"), env_vars.get("HF_HOME")]:
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)