import tkinter as tk
from tkinter import ttk, messagebox
import re

from app.models.auth import Validate, Authentication
from app.models.user_student import Student
from app.gui_app.enrollment_window import EnrollmentWindow
from app.constants import ERRORS

class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#3498db")
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        """Create login window widgets"""
        # Header
        header_frame = tk.Frame(self, bg="#3498db", height=100)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="University Enrollment System", 
            font=("Arial", 24, "bold"),
            bg="#3498db",
            fg="white"
        )
        header_label.pack(pady=30)
        
        # Login Form
        form_frame = tk.Frame(self, bg="#3498db", padx=50, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Login header
        login_label = tk.Label(
            form_frame,
            text="Student Login",
            font=("Arial", 18, "bold"),
            bg="#3498db"
        )
        login_label.pack(pady=(0, 20))
        
        # Email field
        email_frame = tk.Frame(form_frame, bg="#3498db")
        email_frame.pack(fill=tk.X, pady=10)
        
        email_label = tk.Label(
            email_frame,
            text="Email:",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        email_label.pack(side=tk.LEFT)
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            font=("Arial", 12),
            width=30
        )
        email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg="#3498db")
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = tk.Label(
            password_frame,
            text="Password:",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        password_label.pack(side=tk.LEFT)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg="#3498db")
        buttons_frame.pack(pady=20)
        
        login_button = ttk.Button(
            buttons_frame,
            text="Login",
            command=self.login,
            style="WhiteBorder.TButton",
            width=15
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        exit_button = ttk.Button(
            buttons_frame,
            text="Exit",
            command=self.master.quit,
            style="WhiteBorder.TButton",
            width=15
        )
        exit_button.pack(side=tk.LEFT, padx=10)
        
        # Set up styles
        self.configure_styles()
        
        # Footer
        footer_frame = tk.Frame(self, bg="#3498db", height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2025 University Enrollment System",
            font=("Arial", 10),
            bg="#3498db",
            fg="white"
        )
        footer_label.pack(pady=15)
        
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("WhiteBorder.TButton", 
                    background="white",
                    bordercolor="black",
                    lightcolor="white", 
                    darkcolor="white",
                    foreground="black")
            
    def login(self):
        """Handle login process"""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        # Check for empty fields
        if not email or not password:
            messagebox.showerror("Login Error", "Email and password cannot be empty!")
            return
        
        # Validate email format
        if not Validate.validate_email(email):
            messagebox.showerror(
                "Invalid Email", 
                "Email format is invalid! Please use username@university.com format."
            )
            return
        
        # Check if email exists
        if not Validate.check_email_exist(email):
            messagebox.showerror(
                "Login Failed", 
                "Email not found! Please register first."
            )
            return
        
        # Attempt to login
        student = Student(email, password)
        auth_result = True #student.login()
        
        if auth_result is True:
            messagebox.showinfo("Login Successful", f"Welcome, {email}!")
            self.open_enrollment_window(student)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
    
    def open_enrollment_window(self, student):
        """Open enrollment window after successful login"""
        # Clear login window
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # Create enrollment window
        EnrollmentWindow(self.master, student)