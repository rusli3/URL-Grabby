#!/usr/bin/env python3
"""
URL Grabby - Main Application Entry Point

A desktop application for crawling websites and extracting page information
including URLs, titles, and main headings within the same domain.

Author: URL Grabby Team
License: MIT
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path to ensure imports work
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from gui import URLGrabbyGUI
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all required dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        bool: True if all dependencies are available
    """
    required_modules = [
        'customtkinter',
        'requests',
        'bs4',  # beautifulsoup4
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Missing required dependencies:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def main():
    """
    Main application entry point.
    """
    print("=" * 50)
    print("URL Grabby - Web Crawler Application")
    print("Version 1.0.0")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return 1
    
    try:
        # Create and run the GUI application
        print("Starting GUI application...")
        app = URLGrabbyGUI()
        app.run()
        
        print("Application closed successfully.")
        return 0
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        return 0
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this issue if it persists.")
        input("Press Enter to exit...")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)