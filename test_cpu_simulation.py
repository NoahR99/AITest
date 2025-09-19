#!/usr/bin/env python3

"""
Simulation test for AI Generator CPU-only mode with mock dependencies.
This test simulates having PyTorch available and tests the attention_slicing logic.
"""

import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Force CPU mode
os.environ["FORCE_CPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

def create_mock_torch():
    """Create a mock torch module that simulates CPU-only environment."""
    mock_torch = Mock()
    mock_torch.cuda.is_available.return_value = False
    mock_torch.float32 = "float32"
    mock_torch.float16 = "float16"
    
    # Mock generator
    mock_generator = Mock()
    mock_generator.manual_seed.return_value = mock_generator
    mock_torch.Generator.return_value = mock_generator
    
    # Mock backends
    mock_torch.backends.mps.is_available.return_value = False
    
    return mock_torch

def create_mock_pipeline():
    """Create a mock diffusers pipeline."""
    mock_pipeline = Mock()
    mock_pipeline.enable_attention_slicing = Mock()
    mock_pipeline.enable_xformers_memory_efficient_attention = Mock(side_effect=ImportError("xformers not available"))
    mock_pipeline.to.return_value = mock_pipeline
    return mock_pipeline

def test_attention_slicing_fallback():
    """Test that attention_slicing is used when xformers is not available."""
    print("🧪 Testing attention_slicing fallback mechanism...")
    
    try:
        mock_torch = create_mock_torch()
        mock_pipeline = create_mock_pipeline()
        
        with patch.dict('sys.modules', {
            'torch': mock_torch,
            'diffusers': Mock(),
            'PIL': Mock(),
            'cv2': Mock(),
            'numpy': Mock()
        }):
            # Mock the pipeline creation
            with patch('diffusers.StableDiffusionPipeline') as mock_sd_pipeline:
                mock_sd_pipeline.from_pretrained.return_value = mock_pipeline
                
                # Import and test our AI generator
                from ai_generator import AIGenerator
                
                # Initialize generator
                generator = AIGenerator()
                
                # Load a pipeline to trigger the optimization logic
                generator._load_pipeline("text_to_image")
                
                # Verify that attention_slicing was called
                mock_pipeline.enable_attention_slicing.assert_called_once()
                print("✅ attention_slicing was correctly enabled for CPU mode")
                
                # Verify xformers was attempted but failed gracefully
                mock_pipeline.enable_xformers_memory_efficient_attention.assert_called_once()
                print("✅ xformers fallback handled gracefully")
                
                # Verify device is CPU
                assert generator.device == "cpu", f"Expected CPU device, got {generator.device}"
                print("✅ Device correctly detected as CPU")
                
                return True
                
    except Exception as e:
        print(f"❌ Attention slicing test failed: {e}")
        return False

def test_force_cpu_environment():
    """Test that FORCE_CPU environment variable works correctly."""
    print("\n🌍 Testing FORCE_CPU environment variable...")
    
    try:
        mock_torch = create_mock_torch()
        # Make CUDA available but FORCE_CPU should override it
        mock_torch.cuda.is_available.return_value = True
        
        with patch.dict('sys.modules', {'torch': mock_torch}):
            from config import get_device
            
            device = get_device()
            assert device == "cpu", f"Expected CPU device with FORCE_CPU=1, got {device}"
            print("✅ FORCE_CPU environment variable correctly overrides CUDA")
            
            return True
            
    except Exception as e:
        print(f"❌ FORCE_CPU test failed: {e}")
        return False

def test_cpu_optimizations():
    """Test CPU-specific optimizations."""
    print("\n⚡ Testing CPU optimizations...")
    
    try:
        from device_utils import detect_device_capabilities, get_optimized_model_params, setup_performance_environment
        
        # Test that environment is set up for CPU
        setup_performance_environment()
        
        # Check that CUDA is disabled
        assert os.environ.get("CUDA_VISIBLE_DEVICES") == "", "CUDA_VISIBLE_DEVICES not properly disabled"
        print("✅ CUDA_VISIBLE_DEVICES correctly disabled")
        
        # Test capabilities
        capabilities = detect_device_capabilities()
        assert capabilities["device"] == "cpu", "Device not detected as CPU"
        print("✅ Device capabilities correctly detected for CPU")
        
        # Test optimized parameters
        params = get_optimized_model_params(capabilities)
        assert "image" in params and "video" in params, "Optimized parameters not generated"
        print("✅ CPU-optimized parameters generated")
        
        return True
        
    except Exception as e:
        print(f"❌ CPU optimizations test failed: {e}")
        return False

def main():
    """Run simulation tests."""
    print("🧪 AI Generator CPU-Only Simulation Tests")
    print("=" * 50)
    
    tests = [
        test_force_cpu_environment,
        test_cpu_optimizations,
        test_attention_slicing_fallback
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n📊 Simulation Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All simulation tests passed!")
        print("\n✨ Key Validations:")
        print("   • attention_slicing is used instead of xformers")
        print("   • FORCE_CPU environment variable works correctly")
        print("   • CPU optimizations are properly applied")
        print("   • Graceful fallback when xformers is not available")
        return 0
    else:
        print("❌ Some simulation tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())