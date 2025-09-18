#!/bin/bash

# Quick start script for development

echo "🚀 AI Generator Quick Start"
echo "=========================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if we should run tests first
if [ "$1" = "--test" ]; then
    echo "🧪 Running structure tests..."
    python test_structure.py
    if [ $? -ne 0 ]; then
        echo "❌ Tests failed"
        exit 1
    fi
fi

# Create demo files if outputs directory is empty
if [ ! "$(ls -A outputs 2>/dev/null)" ]; then
    echo "📸 Creating demo files..."
    python create_demo.py
fi

# Start the web application
echo "🌐 Starting web application..."
echo "📱 Open your browser to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop"
echo ""

python web_app.py