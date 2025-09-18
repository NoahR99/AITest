@echo off
REM Quick start script for Windows development

echo 🚀 AI Generator Quick Start (Windows)
echo ===================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if we should run tests first
if "%1"=="--test" (
    echo 🧪 Running structure tests...
    python test_structure.py
    if %errorlevel% neq 0 (
        echo ❌ Tests failed
        pause
        exit /b 1
    )
)

REM Create demo files if outputs directory is empty
if not exist "outputs\*" (
    echo 📸 Creating demo files...
    python create_demo.py
)

REM Start the web application
echo 🌐 Starting web application...
echo 📱 Open your browser to: http://localhost:5000
echo ⏹️  Press Ctrl+C to stop
echo.

python web_app.py
pause