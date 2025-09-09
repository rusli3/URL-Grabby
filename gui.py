"""
URL Grabby - GUI Module

This module contains the graphical user interface for the URL Grabby application
built with customtkinter for a modern, responsive design.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import List, Dict
from crawler import URLCrawler
import os


class URLGrabbyGUI:
    """
    Main GUI class for the URL Grabby application.
    
    Provides a modern interface for web crawling with real-time updates,
    progress tracking, and CSV export functionality.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        # Configure customtkinter
        ctk.set_appearance_mode("system")  # "dark" or "light"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("URL Grabby - Web Crawler")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass  # Icon file not found, continue without it
        
        # Initialize crawler
        self.crawler = None
        
        # GUI state variables
        self.is_crawling = False
        
        # Create GUI components
        self._create_widgets()
        self._setup_layout()
        
        # Configure window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        
        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame,
            text="URL Grabby",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Extract URLs, titles, and headings from websites",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        
        # Input section frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        
        # URL input
        self.url_label = ctk.CTkLabel(
            self.input_frame,
            text="Starting URL:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        self.url_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="https://example.com",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        
        # Delay input
        self.delay_label = ctk.CTkLabel(
            self.input_frame,
            text="Request Delay (seconds):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        self.delay_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="1.0",
            width=100,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        
        # Control buttons frame
        self.control_frame = ctk.CTkFrame(self.main_frame)
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="Start Crawling",
            command=self._start_crawling,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2FA572",
            hover_color="#258A5A"
        )
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="Stop Process",
            command=self._stop_crawling,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            state="disabled"
        )
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.control_frame,
            text="Export to CSV",
            command=self._export_data,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            state="disabled"
        )
        
        # Progress section frame
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to start crawling",
            font=ctk.CTkFont(size=12)
        )
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=20
        )
        self.progress_bar.set(0)
        
        # Statistics frame
        self.stats_frame = ctk.CTkFrame(self.progress_frame)
        
        self.visited_label = ctk.CTkLabel(
            self.stats_frame,
            text="Visited: 0",
            font=ctk.CTkFont(size=11)
        )
        
        self.queue_label = ctk.CTkLabel(
            self.stats_frame,
            text="Queue: 0",
            font=ctk.CTkFont(size=11)
        )
        
        self.collected_label = ctk.CTkLabel(
            self.stats_frame,
            text="Collected: 0",
            font=ctk.CTkFont(size=11)
        )
        
        # Log section frame
        self.log_frame = ctk.CTkFrame(self.main_frame)
        
        # Log label
        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="Activity Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        # Log text area with scrollbar
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=200,
            font=ctk.CTkFont(size=10, family="Consolas"),
            wrap="word"
        )
        
        # Clear log button
        self.clear_log_button = ctk.CTkButton(
            self.log_frame,
            text="Clear Log",
            command=self._clear_log,
            height=30,
            width=100,
            font=ctk.CTkFont(size=11)
        )
    
    def _setup_layout(self):
        """Setup the layout of all widgets."""
        
        # Main frame
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.header_label.pack(pady=(0, 5))
        self.subtitle_label.pack(pady=(0, 20))
        
        # Input section
        self.input_frame.pack(fill="x", pady=(0, 15))
        
        # URL input
        self.url_label.pack(anchor="w", padx=20, pady=(15, 5))
        self.url_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Delay input
        self.delay_label.pack(anchor="w", padx=20, pady=(0, 5))
        self.delay_entry.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Control buttons
        self.control_frame.pack(fill="x", pady=(0, 15))
        
        self.start_button.pack(side="left", padx=(20, 10), pady=15)
        self.stop_button.pack(side="left", padx=(0, 10), pady=15)
        self.export_button.pack(side="right", padx=(10, 20), pady=15)
        
        # Progress section
        self.progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_label.pack(pady=(15, 10))
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        
        # Statistics
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.visited_label.pack(side="left", padx=(10, 20), pady=10)
        self.queue_label.pack(side="left", padx=(0, 20), pady=10)
        self.collected_label.pack(side="left", padx=(0, 20), pady=10)
        
        # Log section
        self.log_frame.pack(fill="both", expand=True)
        
        self.log_label.pack(anchor="w", padx=20, pady=(15, 5))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.clear_log_button.pack(anchor="e", padx=20, pady=(0, 15))
    
    def _validate_inputs(self) -> tuple[str, float] | tuple[None, None]:
        """
        Validate user inputs.
        
        Returns:
            tuple: (url, delay) if valid, (None, None) if invalid
        """
        # Get URL
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a starting URL")
            return None, None
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Get delay
        try:
            delay = float(self.delay_entry.get() or "1.0")
            if delay < 0:
                raise ValueError("Delay cannot be negative")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay (number >= 0)")
            return None, None
        
        return url, delay
    
    def _start_crawling(self):
        """Start the crawling process."""
        # Validate inputs
        url, delay = self._validate_inputs()
        if url is None or delay is None:
            return
        
        # Update GUI state
        self.is_crawling = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.export_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.delay_entry.configure(state="disabled")
        
        # Clear previous data
        self._clear_log()
        self.progress_bar.set(0)
        self._update_statistics(0, 0, 0)
        
        # Initialize crawler
        self.crawler = URLCrawler(url, delay)
        
        # Set up crawler callbacks
        self.crawler.set_callbacks(
            log_callback=self._log_message,
            progress_callback=self._update_progress,
            completion_callback=self._crawling_completed
        )
        
        # Start crawling
        if self.crawler.start_crawling():
            self._log_message("Crawling started successfully!")
        else:
            self._log_message("Failed to start crawling!")
            self._stop_crawling()
    
    def _stop_crawling(self):
        """Stop the crawling process."""
        if self.crawler and self.is_crawling:
            self.crawler.stop_crawling()
        
        # Update GUI state
        self.is_crawling = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.url_entry.configure(state="normal")
        self.delay_entry.configure(state="normal")
        
        # Enable export if we have data
        if self.crawler and self.crawler.get_collected_data():
            self.export_button.configure(state="normal")
    
    def _export_data(self):
        """Export collected data to CSV file."""
        if not self.crawler or not self.crawler.get_collected_data():
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save crawled data as..."
        )
        
        if filename:
            if self.crawler.save_to_csv(filename):
                messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
            else:
                messagebox.showerror("Error", "Failed to export data!")
    
    def _log_message(self, message: str):
        """
        Add a message to the log (thread-safe).
        
        Args:
            message (str): Message to add to log
        """
        def update_log():
            self.log_text.insert("end", f"{message}\n")
            self.log_text.see("end")
        
        # Schedule GUI update in main thread
        self.root.after(0, update_log)
    
    def _update_progress(self, visited: int, total: int):
        """
        Update progress bar and statistics (thread-safe).
        
        Args:
            visited (int): Number of URLs visited
            total (int): Total number of URLs discovered
        """
        def update_gui():
            # Update progress bar
            if total > 0:
                progress = visited / total
                self.progress_bar.set(progress)
                self.progress_label.configure(text=f"Progress: {visited}/{total} pages ({progress:.1%})")
            else:
                self.progress_bar.set(0)
                self.progress_label.configure(text="Starting...")
            
            # Update statistics
            if self.crawler:
                stats = self.crawler.get_statistics()
                self._update_statistics(
                    stats['visited_count'],
                    stats['queue_size'],
                    stats['data_count']
                )
        
        # Schedule GUI update in main thread
        self.root.after(0, update_gui)
    
    def _update_statistics(self, visited: int, queue: int, collected: int):
        """
        Update statistics display.
        
        Args:
            visited (int): Number of visited URLs
            queue (int): Number of URLs in queue
            collected (int): Number of data records collected
        """
        self.visited_label.configure(text=f"Visited: {visited}")
        self.queue_label.configure(text=f"Queue: {queue}")
        self.collected_label.configure(text=f"Collected: {collected}")
    
    def _crawling_completed(self, data: List[Dict[str, str]]):
        """
        Handle crawling completion (thread-safe).
        
        Args:
            data (List[Dict[str, str]]): Collected crawling data
        """
        def update_gui():
            self._stop_crawling()
            self.progress_label.configure(text=f"Completed! {len(data)} pages crawled")
            
            if data:
                self.export_button.configure(state="normal")
                messagebox.showinfo("Crawling Complete", 
                                  f"Crawling completed!\n{len(data)} pages were processed.\n\nClick 'Export to CSV' to save the data.")
            else:
                messagebox.showwarning("Crawling Complete", "Crawling completed but no data was collected.")
        
        # Schedule GUI update in main thread
        self.root.after(0, update_gui)
    
    def _clear_log(self):
        """Clear the log text area."""
        self.log_text.delete("1.0", "end")
    
    def _on_closing(self):
        """Handle window close event."""
        if self.is_crawling:
            if messagebox.askokcancel("Quit", "Crawling is in progress. Do you want to stop and quit?"):
                self._stop_crawling()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the GUI application."""
        # Set default values
        self.delay_entry.insert(0, "1.0")
        
        # Log welcome message
        self._log_message("Welcome to URL Grabby!")
        self._log_message("Enter a starting URL and click 'Start Crawling' to begin.")
        self._log_message("The crawler will stay within the same domain and extract page information.")
        self._log_message("-" * 50)
        
        # Start the main loop
        self.root.mainloop()


def main():
    """Main function to run the application."""
    app = URLGrabbyGUI()
    app.run()


if __name__ == "__main__":
    main()