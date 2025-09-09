#!/bin/bash
# URL Grabby - Linux/macOS Shell Launcher
# This script provides an easy way to run URL Grabby on Unix-like systems

echo "========================================"
echo "URL Grabby - Web Crawler Application"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from your package manager or https://python.org"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found"
    echo "Please run this script from the URL Grabby directory"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found, using system Python"
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import customtkinter, requests, bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Some dependencies are missing. Installing..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "Please run: pip install -r requirements.txt"
        echo
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Starting URL Grabby..."
echo
python3 main.py

echo
echo "URL Grabby closed."
read -p "Press Enter to exit..."