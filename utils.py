"""
URL Grabby - Utility Functions

This module contains utility functions and helper classes used throughout
the URL Grabby application.
"""

import os
import re
from urllib.parse import urlparse, urljoin
from typing import Optional, List, Dict, Any
import time
from datetime import datetime


class URLValidator:
    """Utility class for URL validation and normalization."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Check if a URL is valid.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize a URL by adding protocol if missing.
        
        Args:
            url (str): URL to normalize
            
        Returns:
            str: Normalized URL
        """
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url (str): URL to extract domain from
            
        Returns:
            str: Domain or empty string if invalid
        """
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            return ""


class FileManager:
    """Utility class for file operations."""
    
    @staticmethod
    def ensure_directory_exists(file_path: str) -> bool:
        """
        Ensure the directory for a file path exists.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bool: True if directory exists or was created
        """
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """
        Create a safe filename by removing invalid characters.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Safe filename
        """
        # Remove invalid characters
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove control characters
        safe_filename = re.sub(r'[\x00-\x1f\x7f]', '', safe_filename)
        
        # Limit length
        if len(safe_filename) > 200:
            safe_filename = safe_filename[:200]
        
        return safe_filename
    
    @staticmethod
    def generate_timestamp_filename(base_name: str, extension: str = '.csv') -> str:
        """
        Generate a filename with timestamp.
        
        Args:
            base_name (str): Base name for the file
            extension (str): File extension
            
        Returns:
            str: Filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_base = FileManager.get_safe_filename(base_name)
        return f"{safe_base}_{timestamp}{extension}"


class TextProcessor:
    """Utility class for text processing."""
    
    @staticmethod
    def clean_text(text: str, max_length: int = 500) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text (str): Text to clean
            max_length (int): Maximum length of cleaned text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = ' '.join(text.split())
        
        # Remove control characters
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
        
        # Truncate if too long
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length-3] + "..."
        
        return cleaned
    
    @staticmethod
    def extract_domain_name(url: str) -> str:
        """
        Extract a clean domain name from URL for display.
        
        Args:
            url (str): URL to extract domain from
            
        Returns:
            str: Clean domain name
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return domain
        except Exception:
            return "unknown"


class ProgressTracker:
    """Utility class for tracking operation progress."""
    
    def __init__(self):
        """Initialize progress tracker."""
        self.start_time = None
        self.total_items = 0
        self.completed_items = 0
    
    def start(self, total_items: int = 0):
        """
        Start tracking progress.
        
        Args:
            total_items (int): Total number of items to process
        """
        self.start_time = time.time()
        self.total_items = total_items
        self.completed_items = 0
    
    def update(self, completed_items: int):
        """
        Update progress.
        
        Args:
            completed_items (int): Number of completed items
        """
        self.completed_items = completed_items
    
    def get_progress_info(self) -> Dict[str, Any]:
        """
        Get current progress information.
        
        Returns:
            Dict containing progress information
        """
        if not self.start_time:
            return {}
        
        elapsed_time = time.time() - self.start_time
        
        info = {
            'elapsed_time': elapsed_time,
            'completed_items': self.completed_items,
            'total_items': self.total_items,
            'progress_percentage': 0,
            'estimated_time_remaining': 0,
            'items_per_second': 0
        }
        
        if self.total_items > 0:
            info['progress_percentage'] = (self.completed_items / self.total_items) * 100
        
        if elapsed_time > 0:
            info['items_per_second'] = self.completed_items / elapsed_time
            
            if self.total_items > 0 and self.completed_items > 0:
                remaining_items = self.total_items - self.completed_items
                info['estimated_time_remaining'] = remaining_items / info['items_per_second']
        
        return info
    
    def format_time(self, seconds: float) -> str:
        """
        Format time duration for display.
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Formatted time string
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"


class ConfigManager:
    """Utility class for managing application configuration."""
    
    DEFAULT_CONFIG = {
        'default_delay': 1.0,
        'max_pages': 1000,
        'timeout': 10,
        'user_agent': 'URL-Grabby/1.0 (Educational Web Crawler)',
        'export_format': 'csv',
        'log_level': 'info'
    }
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Dict: Default configuration settings
        """
        return cls.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def validate_delay(delay: str) -> float:
        """
        Validate and convert delay value.
        
        Args:
            delay (str): Delay value as string
            
        Returns:
            float: Valid delay value
            
        Raises:
            ValueError: If delay is invalid
        """
        try:
            delay_float = float(delay)
            if delay_float < 0:
                raise ValueError("Delay cannot be negative")
            if delay_float > 60:
                raise ValueError("Delay cannot exceed 60 seconds")
            return delay_float
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Delay must be a valid number")
            raise


# Export utility functions for easy importing
__all__ = [
    'URLValidator',
    'FileManager', 
    'TextProcessor',
    'ProgressTracker',
    'ConfigManager'
]