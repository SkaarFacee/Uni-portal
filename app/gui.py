import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.gui_app.login_window import LoginWindow
from app.models.auth import Validate
from app.constants import USER_CSV_FILE
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class GUIUniApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("University Enrollment System")
        self.geometry("800x600")
        self.configure(bg="#3498db")
        
        # Set app icon if available
        try:
            self.iconbitmap("app/gui/assets/logo.icns")
        except:
            pass
        
        # Center the window
        self.center_window()
        
        # Check if data files exist
        self.check_data_files()
        
        # Initialize login window
        self.open_login_window()
        
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def check_data_files(self):
        """Check if required data files exist"""
        if not os.path.exists(USER_CSV_FILE):
            messagebox.showwarning(
                "Data Files Missing", 
                "Required data files are missing. Please run the CLI app first to initialize them."
            )
    
    def open_login_window(self):
        """Open the login window"""
        # Clear any existing frames
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create login window
        LoginWindow(self)
        
if __name__ == "__main__":
    app = GUIUniApp()
    # bring window to front
    app.lift()  # Brings window to top of stacking order
    app.attributes('-topmost', True)  # Forces window to stay on top temporarily
    app.after_idle(app.attributes, '-topmost', False)  # Disables topmost after window appears
    app.focus_force()  # Forces focus on the window
    app.mainloop()