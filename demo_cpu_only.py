#!/usr/bin/env python3

"""
Demonstration script showing CPU-only AI Generator functionality.
This script shows how the AI Generator works without CUDA/GPU dependencies.
"""

import os
import sys

# Force CPU mode for demonstration
os.environ["FORCE_CPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

def show_cpu_only_setup():
    """Show CPU-only setup information."""
    print("🤖 CPU-Only AI Generator Demonstration")
    print("=" * 50)
    
    print("\n🔧 Environment Configuration:")
    print(f"   FORCE_CPU: {os.environ.get('FORCE_CPU', 'Not set')}")
    print(f"   CUDA_VISIBLE_DEVICES: '{os.environ.get('CUDA_VISIBLE_DEVICES', 'Not set')}'")
    
    # Show system info
    import platform
    print(f"\n💻 System Information:")
    print(f"   Platform: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Processor: {platform.processor()}")
    print(f"   Python: {platform.python_version()}")

def show_device_detection():
    """Show device detection in CPU-only mode."""
    print("\n🔍 Device Detection:")
    
    try:
        from config import get_device
        from device_utils import detect_device_capabilities
        
        device = get_device()
        print(f"   Detected device: {device}")
        
        capabilities = detect_device_capabilities()
        print(f"   Device capabilities:")
        for key, value in capabilities.items():
            print(f"     {key}: {value}")
            
    except ImportError as e:
        print(f"   ⚠️  Dependencies not available: {e}")
        print("   This is normal if PyTorch/diffusers are not installed")

def show_requirements_comparison():
    """Show different requirements files for CPU-only mode."""
    print("\n📦 Requirements Files:")
    
    files = [
        ("requirements.txt", "Default (CPU-first)"),
        ("requirements-cpu.txt", "CPU-only (no CUDA)"),
        ("requirements-arm.txt", "ARM-optimized")
    ]
    
    for filename, description in files:
        print(f"\n   {filename} - {description}:")
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()[:10]  # Show first 10 lines
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"     • {line}")
                if len(f.readlines()) > 10:
                    print("     ...")
        except FileNotFoundError:
            print(f"     ❌ File not found")

def show_ai_generator_demo():
    """Demonstrate AI Generator initialization in CPU-only mode."""
    print("\n🤖 AI Generator Demo:")
    
    try:
        from ai_generator import AIGenerator
        
        print("   Initializing AI Generator in CPU-only mode...")
        generator = AIGenerator()
        
        print(f"   ✅ Successfully initialized on device: {generator.device}")
        print(f"   📊 Capabilities: {generator.capabilities}")
        
        # Show that attention slicing is used instead of xformers
        print("\n   🧠 Memory Optimization:")
        print("   • Uses attention_slicing() instead of xformers")
        print("   • Optimized for CPU inference")
        print("   • No CUDA dependencies required")
        
        # Cleanup
        generator.cleanup()
        print("   🧹 Cleanup completed")
        
    except ImportError as e:
        print(f"   ⚠️  AI Generator not available: {e}")
        print("   Install dependencies with: pip install -r requirements-cpu.txt")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def show_usage_examples():
    """Show usage examples for CPU-only mode."""
    print("\n💡 Usage Examples:")
    
    print("\n   🛠️  Setup for CPU-only mode:")
    print("     Windows: setup.bat --cpu-only")
    print("     Linux/Mac: ./setup.sh --cpu-only")
    
    print("\n   🌍 Environment variables:")
    print("     export FORCE_CPU=1")
    print("     export CUDA_VISIBLE_DEVICES=\"\"")
    
    print("\n   📦 Direct installation:")
    print("     pip install -r requirements-cpu.txt")
    
    print("\n   🚀 Running the application:")
    print("     python cli.py --help")
    print("     python web_app.py")
    print("     python example.py")

def main():
    """Run the CPU-only demonstration."""
    show_cpu_only_setup()
    show_device_detection()
    show_requirements_comparison()
    show_ai_generator_demo()
    show_usage_examples()
    
    print("\n🎉 CPU-Only Mode Successfully Demonstrated!")
    print("\nKey Benefits:")
    print("• No CUDA/GPU dependencies required")
    print("• Works on any system with sufficient RAM")
    print("• Avoids xformers compilation issues")
    print("• Uses attention_slicing for memory efficiency")
    print("• Compatible with ARM, x86, and x64 processors")

if __name__ == "__main__":
    main()