@echo off
title Professor AI Research Assistant

echo.
echo  ____   _    _   _ ____  _   _ 
echo ^|  _ \ / \  ^| \ ^| ^|  _ \^| ^| ^| ^|
echo ^| ^|_) / _ \ ^|  \^| ^| ^| ^| ^| ^| ^| ^|
echo ^|  __/ ___ \^| ^|\  ^| ^|_^| ^| ^|_^| ^|
echo ^|_^| /_/   \_\_^| \_^|____/ \___/ 
echo.
echo AI Research Assistant
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    echo 💡 Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Install requirements if needed
if not exist "venv" (
    echo 🔧 Setting up virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Installing requirements...
    pip install -r requirement.txt
) else (
    call venv\Scripts\activate.bat
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo ❌ .env file not found!
    echo.
    echo 💡 Please create a .env file with your API keys:
    echo    GOOGLE_API_KEY=your_google_api_key_here
    echo    SERPER_API_KEY=your_serper_api_key_here
    echo.
    echo 📖 See README.md for detailed setup instructions
    pause
    exit /b 1
)

echo ✅ Environment ready
echo.

REM Start the application
echo 🚀 Starting Professor AI Research Assistant...
echo 📡 Server will be available at: http://localhost:5000
echo 🔧 Press Ctrl+C to stop the server
echo.

python app.py

pause
