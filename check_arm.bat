@echo off
REM Quick ARM/Snapdragon Detection Script
REM Run this to verify your Surface Laptop is properly detected

echo 🔍 Surface Laptop ARM Detection Tool
echo =====================================
echo.

REM Check Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detected

REM Check system architecture
echo 📱 Checking system architecture...
wmic computersystem get SystemType | findstr /i "ARM" >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ ARM64 processor detected - Snapdragon system confirmed!
    echo 🎯 This system will use ARM-optimized AI settings
) else (
    echo ℹ️  x64 processor detected - Standard settings will be used
)

REM Show system info
echo.
echo 💻 System Information:
wmic computersystem get Model,SystemFamily,SystemSKUNumber /format:list | findstr "="
echo.

REM Check if AI Generator is properly configured
echo 🤖 Testing AI Generator configuration...
python -c "
import sys, os, platform
sys.path.insert(0, os.getcwd())

try:
    from device_utils import detect_device_capabilities
    capabilities = detect_device_capabilities()
    
    print('✅ AI Generator configuration successful')
    print(f'   Device: {capabilities[\"device\"]}')
    print(f'   Optimized for ARM: {capabilities.get(\"arm_optimized\", False)}')
    print(f'   Recommended image size: {capabilities[\"recommended_size\"]}x{capabilities[\"recommended_size\"]}')
    print(f'   Recommended steps: {capabilities[\"recommended_steps\"]}')
    
    if capabilities.get('arm_optimized'):
        print('🎉 Your Surface Laptop is ready for AI generation!')
        print('   The app will automatically use ARM-optimized settings')
    else:
        print('ℹ️  Standard optimization will be used for your system')
        
except Exception as e:
    print(f'❌ Configuration test failed: {e}')
    print('   Please ensure you have run setup.bat first')
"

echo.
echo 📋 Next Steps:
echo 1. Run setup.bat to install dependencies
echo 2. Run: python web_app.py to start the web interface
echo 3. Or run: python cli.py --help for command line usage
echo.
pause