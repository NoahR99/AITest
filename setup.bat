@echo off
REM Enhanced setup script for the AI Generator app on Windows
REM Supports both x64 and ARM64 (Snapdragon) processors

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

REM Detect processor architecture
echo 🔍 Detecting system architecture...
set ARCH=unknown
wmic computersystem get SystemType | findstr /i "ARM" >nul 2>&1
if %errorlevel% == 0 (
    set ARCH=ARM64
    echo 📱 ARM64 processor detected (Snapdragon/ARM-based)
) else (
    set ARCH=x64
    echo 💻 x64 processor detected
)

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

REM Install requirements based on architecture and user preference
echo 📥 Installing requirements for %ARCH% architecture...

REM Check if user wants to force CPU-only mode
set CPU_ONLY=N
if "%1"=="--cpu-only" set CPU_ONLY=Y
if "%1"=="--force-cpu" set CPU_ONLY=Y

REM Prompt user for installation type on x64 systems
if "%ARCH%"=="x64" (
    if "%CPU_ONLY%"=="N" (
        echo.
        echo Choose installation type:
        echo 1. CPU-only (compatible with all systems, no CUDA dependencies)
        echo 2. Default (may include GPU support if available)
        echo.
        set /p CHOICE="Enter your choice (1 or 2): "
        if "!CHOICE!"=="1" set CPU_ONLY=Y
    )
)

if "%CPU_ONLY%"=="Y" (
    echo 🔧 Using CPU-only packages (no CUDA dependencies)...
    pip install -r requirements-cpu.txt
) else if "%ARCH%"=="ARM64" (
    echo 🔧 Using ARM-optimized packages...
    pip install -r requirements-arm.txt
) else (
    echo 🔧 Using default packages...
    pip install -r requirements.txt
)

echo.
echo ✅ Setup complete for %ARCH% system!
echo.
echo To start using the AI Generator:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the CLI tool: python cli.py --help
echo 3. Run the web interface: python web_app.py
echo.
echo 💡 For CPU-only installation, run: setup.bat --cpu-only
echo.
echo Note: The first run will download AI models (several GB), so ensure you have:
echo - A stable internet connection
echo - At least 10GB of free disk space
if "%ARCH%"=="ARM64" (
    echo - ARM64 processor will use CPU-only mode (no CUDA support)
    echo - Consider increasing RAM for better performance on ARM systems
) else (
    if "%CPU_ONLY%"=="Y" (
        echo - CPU-only mode enabled (no GPU acceleration)
        echo - Consider setting FORCE_CPU=1 environment variable for consistency
    ) else (
        echo - GPU with CUDA support (recommended, but CPU mode also works)
    )
)
echo.
pause