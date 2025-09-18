#!/usr/bin/env python3
"""
Simple test script to verify the application structure without requiring heavy dependencies.
"""

import sys
from pathlib import Path
import ast

def check_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def check_file_structure():
    """Check if all required files exist."""
    required_files = [
        'config.py',
        'ai_generator.py', 
        'cli.py',
        'web_app.py',
        'example.py',
        'requirements.txt',
        'setup.sh',
        'README.md',
        '.gitignore'
    ]
    
    required_dirs = [
        'templates'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    return missing_files, missing_dirs

def check_templates():
    """Check if all required template files exist."""
    required_templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/text_to_image.html',
        'templates/image_to_image.html',
        'templates/text_to_video.html',
        'templates/gallery.html'
    ]
    
    missing_templates = []
    for template in required_templates:
        if not Path(template).exists():
            missing_templates.append(template)
    
    return missing_templates

def main():
    """Run all tests."""
    print("🔍 AI Generator Structure Test")
    print("=" * 40)
    
    # Check file structure
    print("\n📁 Checking file structure...")
    missing_files, missing_dirs = check_file_structure()
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    print("✅ All required files and directories present")
    
    # Check templates
    print("\n🌐 Checking web templates...")
    missing_templates = check_templates()
    if missing_templates:
        print(f"❌ Missing templates: {missing_templates}")
        return False
    print("✅ All template files present")
    
    # Check Python syntax
    print("\n🐍 Checking Python syntax...")
    python_files = ['config.py', 'ai_generator.py', 'cli.py', 'web_app.py', 'example.py']
    
    for file_path in python_files:
        valid, error = check_python_syntax(file_path)
        if not valid:
            print(f"❌ Syntax error in {file_path}: {error}")
            return False
        else:
            print(f"✅ {file_path}")
    
    # Check requirements.txt
    print("\n📦 Checking requirements...")
    with open('requirements.txt', 'r') as f:
        requirements = f.read().strip().split('\n')
    
    required_packages = ['torch', 'diffusers', 'transformers', 'flask', 'pillow', 'opencv-python']
    for package in required_packages:
        found = any(req.lower().startswith(package.lower()) for req in requirements)
        if not found:
            print(f"❌ Missing required package: {package}")
            return False
    print(f"✅ Found {len(requirements)} package requirements")
    
    print("\n🎉 All tests passed!")
    print("\nNext steps:")
    print("1. Run: chmod +x setup.sh && ./setup.sh")
    print("2. Activate venv: source venv/bin/activate")
    print("3. Test CLI: python cli.py --help")
    print("4. Start web app: python web_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)