import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import ast

from app.controllers.enrollment_controller import EnrollmentController
from app.gui_app.subject_details_window import SubjectDetailsWindow
from app.models.enrollment import Enrollment
from app.models.subject import Subject
from app.constants import SUBJECT_ID_COL, LANDING_MSGS

class EnrollmentWindow(tk.Frame):
    def __init__(self, master, student):
        super().__init__(master, bg="#3498db")  # Light blue background
        self.master = master
        self.student = student
        
        # Create the enrollment controller
        self.enrollment_controller = EnrollmentController(student)
        
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets
        self.create_widgets()
        
        # Load enrollments
        self.load_enrollments()
        
    def create_widgets(self):
        """Create enrollment window widgets"""
        # Header
        header_frame = tk.Frame(self, bg="#3498db", height=100)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Student Enrollment Management", 
            font=("Arial", 24, "bold"),
            bg="#3498db",
            fg="white"
        )
        header_label.pack(pady=30)
        
        # Navigation Menu
        nav_frame = tk.Frame(self, bg="#3498db", height=50)
        nav_frame.pack(fill=tk.X)
        
        profile_btn = ttk.Button(
            nav_frame,
            text="View Profile",
            command=self.open_profile_window,
            style="WhiteBorder.TButton" 
        )
        profile_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        logout_btn = ttk.Button(
            nav_frame,
            text="Logout",
            command=self.logout,
            style="WhiteBorder.TButton" 
        )
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Main content
        content_frame = tk.Frame(self, bg="#3498db")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Enrollments
        left_frame = tk.Frame(content_frame, bg="#3498db", width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        enrolled_label = tk.Label(
            left_frame,
            text="Your Enrollments",
            font=("Arial", 16, "bold"),
            bg="#3498db"
        )
        enrolled_label.pack(pady=(0, 10), anchor="w")
        
        # Create Treeview for enrollments
        self.enrollment_tree = ttk.Treeview(
            left_frame,
            columns=("subject_id", "mark", "grade"),
            show="headings",
            height=10
        )

        # Define columns
        self.enrollment_tree.heading("subject_id", text="Subject ID")
        self.enrollment_tree.heading("mark", text="Mark")
        self.enrollment_tree.heading("grade", text="Grade")
        
        self.enrollment_tree.column("subject_id", width=150)
        self.enrollment_tree.column("mark", width=100)
        self.enrollment_tree.column("grade", width=100)
        
        self.enrollment_tree.pack(fill=tk.BOTH, expand=True)
        
        
        # Button frame for enrollment actions
        enroll_action_frame = tk.Frame(left_frame, bg="#3498db")
        enroll_action_frame.pack(fill=tk.X, pady=10)
        
        unenroll_btn = ttk.Button(
            enroll_action_frame,
            text="Unenroll Selected",
            command=self.unenroll_selected,
            style="WhiteBorder.TButton" 
        )
        unenroll_btn.pack(side=tk.LEFT, padx=5)
        
        details_btn = ttk.Button(
            enroll_action_frame,
            text="View Details",
            command=self.view_selected_details,
            style="WhiteBorder.TButton" 
        )
        details_btn.pack(side=tk.RIGHT, padx=5)
        
        # Right panel - Available Subjects
        right_frame = tk.Frame(content_frame, bg="#3498db", width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        available_label = tk.Label(
            right_frame,
            text="Available Subjects",
            font=("Arial", 16, "bold"),
            bg="#3498db"
        )
        available_label.pack(pady=(0, 10), anchor="w")
        
        # Create Treeview for available subjects
        self.subjects_tree = ttk.Treeview(
            right_frame,
            columns=("subject_id", "name", "rating"),
            show="headings",
            height=10
        )
        
        # Define columns
        self.subjects_tree.heading("subject_id", text="Subject ID")
        self.subjects_tree.heading("name", text="Course Name")
        self.subjects_tree.heading("rating", text="Rating")
        
        self.subjects_tree.column("subject_id", width=100)
        self.subjects_tree.column("name", width=200)
        self.subjects_tree.column("rating", width=100)
        
        self.subjects_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        scrollbar2 = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.subjects_tree.yview)
        self.subjects_tree.configure(yscroll=scrollbar2.set)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load available subjects
        self.load_available_subjects()
        
        # Button frame for subject actions
        subject_action_frame = tk.Frame(right_frame, bg="#3498db")
        subject_action_frame.pack(fill=tk.X, pady=10)
        
        enroll_btn = ttk.Button(
            subject_action_frame,
            text="Enroll Selected",
            command=self.enroll_selected,
            style="WhiteBorder.TButton" 
        )
        enroll_btn.pack(side=tk.LEFT, padx=5)
        
        random_enroll_btn = ttk.Button(
            subject_action_frame,
            text="Random Enrollment",
            command=self.random_enrollment,
            style="WhiteBorder.TButton" 
        )
        random_enroll_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            subject_action_frame,
            text="Refresh ",
            command=self.refresh_subjects,
            style="WhiteBorder.TButton" 
        )
        refresh_btn.pack(side=tk.LEFT, padx=3)
        
        # Enrollment status
        status_frame = tk.Frame(self, bg="#3498db", height=50)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"Enrolled in 0/4 subjects",
            font=("Arial", 16,  "bold"),
            bg="#3498db"
        )
        self.status_label.pack(pady=15)
        
        # Set up styles
        self.configure_styles()
        
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Button styles
        style.configure("TButton", font=("Arial", 12))
        
        # Create a style for white buttons with black border
        style.configure("WhiteBorder.TButton", 
                    background="white",
                    bordercolor="black",
                    lightcolor="white", 
                    darkcolor="white",
                    foreground="black")
        
        style.configure("Treeview.Heading", 
                    font=("Arial", 10, "bold"),
                    background="#d0d0d0",
                    foreground="black")
        
        style.configure("Treeview", 
                    font=("Arial", 10),
                    background="black",  # Row background
                    foreground="white",  # Text color
                    fieldbackground="black",  # Background behind rows
                    rowheight=25)  # Increase row height
        
    def load_enrollments(self):
        """Load current enrollments into the treeview"""
        # Clear existing items
        for item in self.enrollment_tree.get_children():
            self.enrollment_tree.delete(item)
        
        # Get enrolled subjects
        enrollments = self.enrollment_controller.enrollment.view_enrollments()
        
        # Add to treeview
        for subject_id, (mark, grade) in enrollments.items():
            self.enrollment_tree.insert("", "end", values=(subject_id, mark, grade))
        
        # Update status label
        enrollment_count = self.enrollment_controller.enrollment.get_number_of_enrollments()
        self.status_label.config(text=f"Enrolled in {enrollment_count}/4 subjects")
            
    def load_available_subjects(self):
        """Load available subjects into the treeview"""
        # Clear existing items
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)
            
        # Get all courses
        courses_df = self.enrollment_controller.enrollment.courses_df
        
        # Get IDs of already enrolled subjects
        enrolled_ids = list(self.enrollment_controller.enrollment.view_enrollments().keys())
        
        # Filter out already enrolled subjects
        available_courses = courses_df[~courses_df[SUBJECT_ID_COL].isin(enrolled_ids)]
        
        # Add to treeview
        for _, row in available_courses.iterrows():
            self.subjects_tree.insert("", "end", values=(
                row[SUBJECT_ID_COL], 
                row['Course Name'], 
                row['Course Rating']
            ))
    
    def enroll_selected(self):
        """Enroll in selected subject"""
        # Check if maximum enrollments reached
        if self.enrollment_controller.enrollment.get_number_of_enrollments() >= 4:
            messagebox.showerror(
                "Enrollment Error", 
                "You have already enrolled in the maximum number of subjects (4)."
            )
            return
            
        # Get selected subject
        selected_item = self.subjects_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a subject to enroll in.")
            return
            
        subject_id = self.subjects_tree.item(selected_item[0], "values")[0]
        # Enroll in subject
        result = self.enrollment_controller.enrollment.enroll_subject(subject_id)
        
        if result:
            messagebox.showinfo("Enrollment Successful", f"Successfully enrolled in subject {subject_id}.")
            # Refresh views
            self.load_enrollments()
            self.load_available_subjects()
        else:
            messagebox.showerror("Enrollment Failed", "Failed to enroll in the subject.")
    
    def random_enrollment(self):
        """Enroll in random subjects"""
        # Check if maximum enrollments reached
        if self.enrollment_controller.enrollment.get_number_of_enrollments() >= 4:
            messagebox.showerror(
                "Enrollment Error", 
                "You have already enrolled in the maximum number of subjects (4)."
            )
            return
        
        # Confirm random enrollment
        confirm = messagebox.askyesno(
            "Random Enrollment", 
            "Do you want to randomly enroll in subjects up to the maximum of 4?"
        )
        
        if confirm:
            result = self.enrollment_controller.enrollment.add_random_enroll()
            if result:
                messagebox.showinfo(
                    "Random Enrollment Successful", 
                    "Successfully enrolled in random subjects."
                )
                # Refresh views
                self.load_enrollments()
                self.load_available_subjects()
            else:
                messagebox.showerror(
                    "Enrollment Failed", 
                    "Failed to enroll in random subjects. You may have reached the maximum of 4 subjects."
                )
    
    def unenroll_selected(self):
        """Unenroll from selected subject"""
        # Get selected subject
        selected_item = self.enrollment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a subject to unenroll from.")
            return
            
        subject_id = self.enrollment_tree.item(selected_item[0], "values")[0]
        
        # Confirm action
        confirm = messagebox.askyesno(
            "Confirm Unenrollment", 
            f"Are you sure you want to unenroll from subject {subject_id}?"
        )
        
        if not confirm:
            return
            
        # Unenroll from subject
        result = self.enrollment_controller.enrollment.unenroll_subject(subject_id)
        
        if result:
            messagebox.showinfo("Unenrollment Successful", f"Successfully unenrolled from subject {subject_id}.")
            # Refresh views
            self.load_enrollments()
            self.load_available_subjects()
        else:
            messagebox.showerror("Unenrollment Failed", "Failed to unenroll from the subject.")
    
    def view_selected_details(self):
        """View details of selected subject"""
        # Get selected subject
        selected_item = self.enrollment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a subject to view details.")
            return
            
        subject_id = self.enrollment_tree.item(selected_item[0], "values")[0]
        mark = float(self.enrollment_tree.item(selected_item[0], "values")[1])
        
        # Create subject object
        subject = Subject(subject_id, mark)
        
        # Get course info
        if subject.get_course_info(self.enrollment_controller.enrollment.courses_df):
            # Open details window
            SubjectDetailsWindow(self,subject)
        else:
            messagebox.showerror("Error", "Could not retrieve subject details.")
    
    def view_subject_details(self, event):
        """Handle double-click on enrollment treeview"""
        self.view_selected_details()
    
    def refresh_subjects(self):
        """Refresh subject lists"""
        self.load_enrollments()
        self.load_available_subjects()
    
    def open_profile_window(self):
        """Open profile window"""
        self.open_profile_details_window()
    
    def open_profile_details_window(self):
        """Open a new window with profile details"""
        profile_window = tk.Toplevel(self.master)
        profile_window.title("Student Profile")
        profile_window.geometry("500x400")
        profile_window.configure(bg="#3498db")
        
        # Make this window modal
        profile_window.transient(self.master)
        profile_window.grab_set()
        
        # Center the window
        profile_window.update_idletasks()
        width = profile_window.winfo_width()
        height = profile_window.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (height // 2)
        profile_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header_frame = tk.Frame(profile_window, bg="#3498db", height=80)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Student Profile", 
            font=("Arial", 20, "bold"),
            bg="#3498db",
            fg="white"
        )
        header_label.pack(pady=20)
        
        # Profile info
        profile_frame = tk.Frame(profile_window, bg="#3498db", padx=30, pady=20)
        profile_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get profile data
        profile_df = self.enrollment_controller.enrollment.get_student_profile()
        
        if not profile_df.empty:
            row = profile_df.iloc[0]
            
            # Student ID
            id_frame = tk.Frame(profile_frame, bg="#3498db")
            id_frame.pack(fill=tk.X, pady=10)
            
            id_label = tk.Label(
                id_frame,
                text="Student ID:",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                width=15,
                anchor="w"
            )
            id_label.pack(side=tk.LEFT)
            
            id_value = tk.Label(
                id_frame,
                text=row['StudentID'],
                font=("Arial", 12),
                bg="#3498db"
            )
            id_value.pack(side=tk.LEFT, fill=tk.X)
            
            # First Name
            fname_frame = tk.Frame(profile_frame, bg="#3498db")
            fname_frame.pack(fill=tk.X, pady=10)
            
            fname_label = tk.Label(
                fname_frame,
                text="First Name:",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                width=15,
                anchor="w"
            )
            fname_label.pack(side=tk.LEFT)
            
            fname_value = tk.Label(
                fname_frame,
                text=row['FirstName'],
                font=("Arial", 12),
                bg="#3498db"
            )
            fname_value.pack(side=tk.LEFT, fill=tk.X)
            
            # Last Name
            lname_frame = tk.Frame(profile_frame, bg="#3498db")
            lname_frame.pack(fill=tk.X, pady=10)
            
            lname_label = tk.Label(
                lname_frame,
                text="Last Name:",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                width=15,
                anchor="w"
            )
            lname_label.pack(side=tk.LEFT)
            
            lname_value = tk.Label(
                lname_frame,
                text=row['LastName'],
                font=("Arial", 12),
                bg="#3498db"
            )
            lname_value.pack(side=tk.LEFT, fill=tk.X)
            
            # Email
            email_frame = tk.Frame(profile_frame, bg="#3498db")
            email_frame.pack(fill=tk.X, pady=10)
            
            email_label = tk.Label(
                email_frame,
                text="Email:",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                width=15,
                anchor="w"
            )
            email_label.pack(side=tk.LEFT)
            
            email_value = tk.Label(
                email_frame,
                text=row['Email'],
                font=("Arial", 12),
                bg="#3498db"
            )
            email_value.pack(side=tk.LEFT, fill=tk.X)
            
            # Enrollment count
            enroll_frame = tk.Frame(profile_frame, bg="#3498db")
            enroll_frame.pack(fill=tk.X, pady=10)
            
            enroll_label = tk.Label(
                enroll_frame,
                text="Enrollments:",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                width=15,
                anchor="w"
            )
            enroll_label.pack(side=tk.LEFT)
            
            enroll_count = self.enrollment_controller.enrollment.get_number_of_enrollments()
            enroll_value = tk.Label(
                enroll_frame,
                text=f"{enroll_count}/4 subjects",
                font=("Arial", 12),
                bg="#3498db"
            )
            enroll_value.pack(side=tk.LEFT, fill=tk.X)
        else:
            error_label = tk.Label(
                profile_frame,
                text="Error loading profile data",
                font=("Arial", 14, "bold"),
                fg="red",
                bg="#3498db"
            )
            error_label.pack(pady=50)
        
        # Close button
        close_button = ttk.Button(
            profile_window,
            text="Close",
            command=profile_window.destroy,
            style="WhiteBorder.TButton",
            width=15
        )
        close_button.pack(pady=20)
    

    
    def logout(self):
        """Handle logout"""
        self.student.logout()
        messagebox.showinfo("Logout", "You have been successfully logged out.")
        # Call the master's open_login_window method
        if hasattr(self.master, 'open_login_window'):
            self.master.open_login_window()
        else:
            # Fallback if the method doesn't exist
            self.master.destroy()
            from app.gui_app.login_window import LoginWindow
            LoginWindow(tk.Tk())