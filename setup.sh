#!/bin/bash

# Simple setup script for the AI Generator app

echo "🤖 AI Generator Setup Script"
echo "=============================="

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1-2)
if [ -z "$python_version" ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
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

# Check if user wants CPU-only installation
CPU_ONLY=false
if [ "$1" = "--cpu-only" ] || [ "$1" = "--force-cpu" ]; then
    CPU_ONLY=true
fi

# Detect architecture
ARCH=$(uname -m)
echo "🔍 Detected architecture: $ARCH"

# Choose requirements file based on options and architecture
if [ "$CPU_ONLY" = true ]; then
    echo "🔧 Using CPU-only packages (no CUDA dependencies)..."
    pip install -r requirements-cpu.txt
elif [[ "$ARCH" == "arm"* ]] || [[ "$ARCH" == "aarch64" ]]; then
    echo "🔧 Using ARM-optimized packages..."
    pip install -r requirements-arm.txt
else
    echo "🔧 Using default packages..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start using the AI Generator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the CLI tool: python cli.py --help"
echo "3. Run the web interface: python web_app.py"
echo ""
echo "💡 For CPU-only installation, run: ./setup.sh --cpu-only"
echo ""
echo "Note: The first run will download AI models (several GB), so ensure you have:"
echo "- A stable internet connection"
echo "- At least 10GB of free disk space"
if [ "$CPU_ONLY" = true ]; then
    echo "- CPU-only mode enabled (no GPU acceleration)"
    echo "- Consider setting FORCE_CPU=1 environment variable for consistency"
elif [[ "$ARCH" == "arm"* ]] || [[ "$ARCH" == "aarch64" ]]; then
    echo "- ARM processor will use CPU-only mode (no CUDA support)"
else
    echo "- GPU with CUDA support (recommended, but CPU mode also works)"
fi
echo ""