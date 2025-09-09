"""
URL Grabby - Web Crawler Module

This module contains the core crawling logic for extracting URLs, titles, 
and main headings from web pages within the same domain.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import threading
from typing import Set, List, Dict, Callable, Optional
import csv


class URLCrawler:
    """
    A web crawler that extracts page information from a given domain.
    
    This crawler stays within the same domain as the starting URL and extracts:
    - Page URLs
    - Page titles (<title> tag)
    - Main headings (first <h1> tag)
    """
    
    def __init__(self, start_url: str, delay: float = 1.0):
        """
        Initialize the crawler with a starting URL and request delay.
        
        Args:
            start_url (str): The initial URL to start crawling from
            delay (float): Delay in seconds between requests (default: 1.0)
        """
        self.start_url = start_url
        self.delay = delay
        self.domain = self._extract_domain(start_url)
        
        # Thread-safe collections for tracking URLs
        self.urls_to_visit: Set[str] = {start_url}
        self.visited_urls: Set[str] = set()
        self.collected_data: List[Dict[str, str]] = []
        
        # Threading control
        self.is_running = False
        self.crawler_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Callback functions for GUI updates
        self.log_callback: Optional[Callable[[str], None]] = None
        self.progress_callback: Optional[Callable[[int, int], None]] = None
        self.completion_callback: Optional[Callable[[List[Dict[str, str]]], None]] = None
        
        # Request session for connection reuse
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'URL-Grabby/1.0 (Educational Web Crawler)'
        })
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract the domain from a URL.
        
        Args:
            url (str): The URL to extract domain from
            
        Returns:
            str: The domain (e.g., 'example.com')
        """
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            return ""
    
    def _is_same_domain(self, url: str) -> bool:
        """
        Check if a URL belongs to the same domain as the starting URL.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL is in the same domain
        """
        return self._extract_domain(url) == self.domain
    
    def _normalize_url(self, base_url: str, url: str) -> str:
        """
        Convert relative URLs to absolute URLs and normalize them.
        
        Args:
            base_url (str): The base URL for resolving relative URLs
            url (str): The URL to normalize
            
        Returns:
            str: The normalized absolute URL
        """
        # Join relative URLs with base URL
        absolute_url = urljoin(base_url, url)
        
        # Parse and reconstruct to normalize
        parsed = urlparse(absolute_url)
        
        # Remove fragment (anchor) and normalize
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # Add query string if present
        if parsed.query:
            normalized += f"?{parsed.query}"
            
        return normalized
    
    def _log_message(self, message: str) -> None:
        """
        Send log message to GUI callback if available.
        
        Args:
            message (str): Message to log
        """
        if self.log_callback:
            self.log_callback(message)
    
    def _update_progress(self, visited: int, total: int) -> None:
        """
        Update progress information to GUI callback if available.
        
        Args:
            visited (int): Number of URLs visited
            total (int): Total number of URLs discovered
        """
        if self.progress_callback:
            self.progress_callback(visited, total)
    
    def _extract_page_data(self, url: str, html_content: str) -> Dict[str, str]:
        """
        Extract title and main heading from HTML content.
        
        Args:
            url (str): The URL of the page
            html_content (str): The HTML content
            
        Returns:
            Dict[str, str]: Dictionary with URL, title, and heading
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract page title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        # Extract first h1 tag
        h1_tag = soup.find('h1')
        heading = h1_tag.get_text(strip=True) if h1_tag else ""
        
        return {
            'url': url,
            'title': title,
            'heading': heading
        }
    
    def _extract_links(self, base_url: str, html_content: str) -> Set[str]:
        """
        Extract all links from HTML content that belong to the same domain.
        
        Args:
            base_url (str): The base URL for resolving relative links
            html_content (str): The HTML content
            
        Returns:
            Set[str]: Set of normalized URLs from the same domain
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Find all anchor tags with href attributes
        for link_tag in soup.find_all('a', href=True):
            href = link_tag.get('href') if hasattr(link_tag, 'get') else None
            if not href:
                continue
            
            # Convert to string if needed
            href_str = str(href) if not isinstance(href, str) else href
            
            # Skip non-HTTP(S) protocols
            if href_str.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                continue
            
            try:
                # Normalize the URL
                absolute_url = self._normalize_url(base_url, href_str)
                
                # Only add if it's in the same domain
                if self._is_same_domain(absolute_url):
                    links.add(absolute_url)
                    
            except Exception as e:
                self._log_message(f"Error processing link '{href_str}': {str(e)}")
        
        return links
    
    def _crawl_page(self, url: str) -> bool:
        """
        Crawl a single page and extract data and links.
        
        Args:
            url (str): URL to crawl
            
        Returns:
            bool: True if page was successfully crawled
        """
        try:
            self._log_message(f"Crawling: {url}")
            
            # Make HTTP request
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'html' not in content_type:
                self._log_message(f"Skipping non-HTML content: {url}")
                return False
            
            html_content = response.text
            
            # Extract page data
            page_data = self._extract_page_data(url, html_content)
            self.collected_data.append(page_data)
            
            self._log_message(f"✓ Extracted data from: {url}")
            self._log_message(f"  Title: {page_data['title'][:50]}...")
            
            # Extract new links
            new_links = self._extract_links(url, html_content)
            
            # Add new links to crawl queue
            new_count = 0
            for link in new_links:
                if link not in self.visited_urls and link not in self.urls_to_visit:
                    self.urls_to_visit.add(link)
                    new_count += 1
            
            if new_count > 0:
                self._log_message(f"  Found {new_count} new links")
            
            return True
            
        except requests.RequestException as e:
            self._log_message(f"✗ Request error for {url}: {str(e)}")
            return False
        except Exception as e:
            self._log_message(f"✗ Unexpected error for {url}: {str(e)}")
            return False
    
    def _crawl_loop(self) -> None:
        """
        Main crawling loop that processes URLs until stopped or queue is empty.
        """
        try:
            self._log_message("Starting crawl process...")
            self._log_message(f"Target domain: {self.domain}")
            self._log_message(f"Request delay: {self.delay} seconds")
            
            while self.urls_to_visit and not self._stop_event.is_set():
                # Get next URL to crawl
                current_url = self.urls_to_visit.pop()
                
                # Skip if already visited
                if current_url in self.visited_urls:
                    continue
                
                # Mark as visited
                self.visited_urls.add(current_url)
                
                # Crawl the page
                self._crawl_page(current_url)
                
                # Update progress
                total_discovered = len(self.visited_urls) + len(self.urls_to_visit)
                self._update_progress(len(self.visited_urls), total_discovered)
                
                # Check if we should stop
                if self._stop_event.is_set():
                    break
                
                # Delay between requests
                if self.delay > 0:
                    time.sleep(self.delay)
            
            # Crawling completed
            if self._stop_event.is_set():
                self._log_message("Crawling stopped by user")
            else:
                self._log_message("Crawling completed - all pages processed")
            
            self._log_message(f"Total pages crawled: {len(self.collected_data)}")
            
            # Notify completion
            if self.completion_callback:
                self.completion_callback(self.collected_data)
                
        except Exception as e:
            self._log_message(f"Critical error in crawl loop: {str(e)}")
        finally:
            self.is_running = False
    
    def start_crawling(self) -> bool:
        """
        Start the crawling process in a separate thread.
        
        Returns:
            bool: True if crawling started successfully
        """
        if self.is_running:
            self._log_message("Crawling is already running!")
            return False
        
        # Validate starting URL
        if not self.domain:
            self._log_message("Invalid starting URL!")
            return False
        
        # Reset state
        self.is_running = True
        self._stop_event.clear()
        self.visited_urls.clear()
        self.collected_data.clear()
        self.urls_to_visit = {self.start_url}
        
        # Start crawler thread
        self.crawler_thread = threading.Thread(target=self._crawl_loop, daemon=True)
        self.crawler_thread.start()
        
        return True
    
    def stop_crawling(self) -> None:
        """
        Stop the crawling process.
        """
        if self.is_running:
            self._log_message("Stopping crawl process...")
            self._stop_event.set()
            
            # Wait for thread to finish (with timeout)
            if self.crawler_thread and self.crawler_thread.is_alive():
                self.crawler_thread.join(timeout=5)
    
    def set_callbacks(self, 
                     log_callback: Optional[Callable[[str], None]] = None,
                     progress_callback: Optional[Callable[[int, int], None]] = None,
                     completion_callback: Optional[Callable[[List[Dict[str, str]]], None]] = None) -> None:
        """
        Set callback functions for GUI updates.
        
        Args:
            log_callback: Function to call for log messages
            progress_callback: Function to call for progress updates (visited, total)
            completion_callback: Function to call when crawling completes
        """
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
    
    def save_to_csv(self, filename: str) -> bool:
        """
        Save collected data to a CSV file.
        
        Args:
            filename (str): Path to the CSV file
            
        Returns:
            bool: True if saved successfully
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not self.collected_data:
                    self._log_message("No data to save!")
                    return False
                
                fieldnames = ['URL', 'Page Title', 'Main Heading']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data
                for data in self.collected_data:
                    writer.writerow({
                        'URL': data['url'],
                        'Page Title': data['title'],
                        'Main Heading': data['heading']
                    })
                
                self._log_message(f"✓ Data saved to: {filename}")
                self._log_message(f"  {len(self.collected_data)} pages exported")
                return True
                
        except Exception as e:
            self._log_message(f"✗ Error saving CSV: {str(e)}")
            return False
    
    def get_collected_data(self) -> List[Dict[str, str]]:
        """
        Get the currently collected data.
        
        Returns:
            List[Dict[str, str]]: List of collected page data
        """
        return self.collected_data.copy()
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get crawling statistics.
        
        Returns:
            Dict[str, int]: Statistics including visited count, queue size, and data count
        """
        return {
            'visited_count': len(self.visited_urls),
            'queue_size': len(self.urls_to_visit),
            'data_count': len(self.collected_data)
        }