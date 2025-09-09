# Contributing to URL Grabby

Thank you for your interest in contributing to URL Grabby! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this standard.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/yourusername/url-grabby/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/url-grabby.git
   cd url-grabby
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. **Code Style**: Follow PEP 8 guidelines
2. **Documentation**: Update docstrings and comments
3. **Testing**: Test your changes thoroughly
4. **Commits**: Use clear, descriptive commit messages

### Code Guidelines

- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small
- Handle exceptions appropriately
- Follow existing naming conventions

### Submitting Changes

1. Push your changes to your fork
2. Create a Pull Request with:
   - Clear title and description
   - Link to related issues
   - Screenshots for UI changes
   - List of changes made

### Review Process

1. Automated checks will run
2. Maintainers will review your code
3. Address any feedback
4. Once approved, changes will be merged

## Development Guidelines

### Project Structure

```
url-grabby/
├── main.py          # Application entry point
├── gui.py           # GUI implementation
├── crawler.py       # Core crawling logic
├── utils.py         # Utility functions
├── requirements.txt # Dependencies
├── README.md        # Project documentation
└── assets/          # Images and resources
```

### Adding New Features

1. **GUI Features**: Update `gui.py` and ensure thread safety
2. **Crawler Features**: Modify `crawler.py` with proper error handling
3. **Utilities**: Add reusable functions to `utils.py`

### Testing

Before submitting:

1. Test the GUI with various URLs
2. Test error conditions (invalid URLs, network issues)
3. Test on different operating systems if possible
4. Verify CSV export functionality

### Performance Considerations

- Use threading for long-running operations
- Implement proper request delays
- Handle memory usage for large crawls
- Provide progress feedback

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion for broader topics
- Contact maintainers directly

Thank you for contributing!