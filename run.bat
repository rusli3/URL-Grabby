@echo off
REM URL Grabby - Windows Batch Launcher
REM This script provides an easy way to run URL Grabby on Windows

echo ========================================
echo URL Grabby - Web Crawler Application
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: main.py not found
    echo Please run this script from the URL Grabby directory
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import customtkinter, requests, bs4" >nul 2>&1
if errorlevel 1 (
    echo Some dependencies are missing. Installing...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo Starting URL Grabby...
echo.
python main.py

echo.
echo URL Grabby closed.
pause