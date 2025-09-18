@echo off
REM Simple setup script for the AI Generator app on Windows

echo 🤖 AI Generator Setup Script (Windows)
echo =======================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📈 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo To start using the AI Generator:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the CLI tool: python cli.py --help
echo 3. Run the web interface: python web_app.py
echo.
echo Note: The first run will download AI models (several GB), so ensure you have:
echo - A stable internet connection
echo - At least 10GB of free disk space
echo - GPU with CUDA support (recommended)
echo.
pause