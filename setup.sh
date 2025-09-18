#!/bin/bash

# Simple setup script for the AI Generator app

echo "🤖 AI Generator Setup Script"
echo "=============================="

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1-2)
if [ -z "$python_version" ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start using the AI Generator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the CLI tool: python cli.py --help"
echo "3. Run the web interface: python web_app.py"
echo ""
echo "Note: The first run will download AI models (several GB), so ensure you have:"
echo "- A stable internet connection"
echo "- At least 10GB of free disk space"
echo "- GPU with CUDA support (recommended)"
echo ""