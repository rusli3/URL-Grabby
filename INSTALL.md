# Installation Guide

This guide provides detailed installation instructions for URL Grabby on different operating systems.

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 100MB free space
- **Network**: Internet connection for crawling

## Installation Methods

### Method 1: Quick Start (Recommended)

1. **Download or Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/url-grabby.git
   cd url-grabby
   ```

2. **Run the Launcher**
   - **Windows**: Double-click `run.bat` or run in Command Prompt
   - **macOS/Linux**: Run `./run.sh` in terminal (make executable first: `chmod +x run.sh`)

The launcher will automatically:
- Check Python installation
- Create virtual environment if needed
- Install dependencies
- Start the application

### Method 2: Manual Installation

#### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://python.org)
2. Run installer and check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install python3 python3-pip
```

#### Step 2: Set Up Project

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/url-grabby.git
   cd url-grabby
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python main.py
   ```

### Method 3: Using pip (Future Release)

```bash
pip install url-grabby
url-grabby
```

*Note: This method will be available in future releases when the package is published to PyPI.*

## Troubleshooting

### Common Issues

#### Python Not Found
**Windows:**
- Ensure Python is installed and added to PATH
- Try using `py` instead of `python`

**macOS/Linux:**
- Use `python3` instead of `python`
- Check if Python is installed: `which python3`

#### Permission Errors
**macOS/Linux:**
```bash
chmod +x run.sh
```

**All Systems:**
- Don't use `sudo` with pip in virtual environment
- Use `--user` flag if installing globally: `pip install --user -r requirements.txt`

#### Dependencies Installation Failed

1. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install dependencies individually:**
   ```bash
   pip install customtkinter
   pip install requests
   pip install beautifulsoup4
   ```

3. **For lxml issues (optional):**
   ```bash
   # Skip lxml if it fails to install
   # The application works fine with html.parser
   ```

#### GUI Not Displaying

1. **Check display environment (Linux):**
   ```bash
   echo $DISPLAY
   # If empty, you may need X11 forwarding for SSH
   ```

2. **Virtual machine issues:**
   - Ensure GUI support is enabled
   - Install display drivers if needed

#### Import Errors

1. **Verify virtual environment is activated**
2. **Reinstall dependencies:**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

### Performance Optimization

#### For Large Crawls
- Increase request delay to avoid server overload
- Monitor memory usage
- Consider running in smaller batches

#### For Slow Networks
- Increase timeout values in crawler settings
- Use appropriate request delays

## Development Installation

For developers who want to contribute:

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/url-grabby.git
   cd url-grabby
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```

4. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   # Add any development tools you need
   ```

## Uninstallation

### Virtual Environment Installation
Simply delete the project folder:
```bash
rm -rf url-grabby/  # Linux/macOS
rmdir /s url-grabby  # Windows
```

### Global Installation
```bash
pip uninstall url-grabby
```

## Getting Help

If you encounter issues not covered here:

1. Check the [FAQ](README.md#faq) in the README
2. Search [existing issues](https://github.com/yourusername/url-grabby/issues)
3. Create a [new issue](https://github.com/yourusername/url-grabby/issues/new) with:
   - Your operating system and version
   - Python version (`python --version`)
   - Error message (full traceback)
   - Steps to reproduce

## Next Steps

After installation:
1. Read the [User Guide](README.md#usage) in the README
2. Try crawling a simple website
3. Explore the configuration options
4. Join our community discussions

Happy crawling! 🕷️