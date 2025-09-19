#!/usr/bin/env python3
"""
Test script to validate ARM/Snapdragon compatibility improvements.
This script tests device detection and configuration without requiring all dependencies.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_device_detection():
    """Test the device detection functionality."""
    print("🔍 Testing device detection...")
    
    try:
        from device_utils import detect_device_capabilities, setup_performance_environment
        
        # Setup environment
        setup_performance_environment()
        print("✅ Performance environment setup successful")
        
        # Detect capabilities
        capabilities = detect_device_capabilities()
        print(f"✅ Device capabilities detected: {capabilities}")
        
        # Check ARM detection
        import platform
        machine = platform.machine().lower()
        processor = platform.processor().lower()
        is_arm = any(arch in machine for arch in ['arm', 'aarch64']) or 'arm' in processor
        
        print(f"📱 Architecture: {machine}")
        print(f"🔧 Processor: {processor}")
        print(f"🎯 ARM detected: {is_arm}")
        
        if is_arm:
            print("🔧 ARM-specific optimizations should be active")
            assert capabilities.get("arm_optimized", False), "ARM optimizations not detected"
        
        return True
        
    except Exception as e:
        print(f"❌ Device detection test failed: {e}")
        return False

def test_config_loading():
    """Test the configuration loading."""
    print("\n📝 Testing configuration loading...")
    
    try:
        # Test without PyTorch first
        import config
        print("✅ Config module loaded successfully")
        
        # Test device function exists
        assert hasattr(config, 'get_device'), "get_device function not found"
        print("✅ get_device function available")
        
        # Test capabilities
        assert hasattr(config, 'DEVICE_CAPABILITIES'), "DEVICE_CAPABILITIES not found"
        print(f"✅ Device capabilities loaded: {config.DEVICE_CAPABILITIES}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_requirements_files():
    """Test that requirements files exist and are valid."""
    print("\n📦 Testing requirements files...")
    
    try:
        # Check regular requirements (now CPU-first)
        with open('requirements.txt', 'r') as f:
            content = f.read()
            assert 'torch' in content, "PyTorch not found in requirements"
            assert 'index-url' in content and 'cpu' in content, "CPU-first PyTorch not configured"
            print("✅ Regular requirements.txt validated")
        
        # Check CPU-only requirements
        with open('requirements-cpu.txt', 'r') as f:
            content = f.read()
            assert 'torch' in content, "PyTorch not found in CPU requirements"
            assert 'index-url' in content and 'cpu' in content, "CPU PyTorch index not found"
            print("✅ CPU requirements.txt validated")
        
        # Check ARM requirements
        with open('requirements-arm.txt', 'r') as f:
            content = f.read()
            assert 'torch' in content, "PyTorch not found in ARM requirements"
            assert 'ARM64' in content, "ARM64 reference not found"
            print("✅ ARM requirements.txt validated")
        
        return True
        
    except Exception as e:
        print(f"❌ Requirements files test failed: {e}")
        return False

def test_setup_script():
    """Test that setup script exists and contains ARM detection."""
    print("\n🛠️  Testing setup script...")
    
    try:
        with open('setup.bat', 'r') as f:
            content = f.read()
            assert 'ARM' in content.upper(), "ARM detection not found in setup script"
            assert 'requirements-arm.txt' in content, "ARM requirements not referenced"
            print("✅ Setup script contains ARM support")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup script test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 ARM/Snapdragon Compatibility Test Suite")
    print("=" * 50)
    
    tests = [
        test_device_detection,
        test_config_loading,
        test_requirements_files,
        test_setup_script
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
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! ARM/Snapdragon support is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())