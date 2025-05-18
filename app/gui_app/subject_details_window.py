import tkinter as tk
from tkinter import ttk, messagebox

from app.models.subject import Subject

class SubjectDetailsWindow(tk.Toplevel):
    def __init__(self, master, subject):
        super().__init__(master)
        self.subject = subject
        
        self.title(f"Subject Details - {subject.subject_id}")
        self.geometry("600x600")
        self.configure(bg="#3498db")
        
        # Make this window modal
        self.transient(master)
        self.grab_set()
        
        # Center the window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the parent"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create subject details window widgets"""
        # Header
        header_frame = tk.Frame(self, bg="#3498db", height=80)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text=f"{self.subject.get_name()}", 
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white"
        )
        header_label.pack(pady=20)
        
        # Details content
        content_frame = tk.Frame(self, bg="#3498db", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Subject ID
        id_frame = tk.Frame(content_frame, bg="#3498db")
        id_frame.pack(fill=tk.X, pady=10)
        
        id_label = tk.Label(
            id_frame,
            text="Subject ID:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        id_label.pack(side=tk.LEFT)
        
        id_value = tk.Label(
            id_frame,
            text=self.subject.subject_id,
            font=("Arial", 12),
            bg="#3498db"
        )
        id_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Course Name
        name_frame = tk.Frame(content_frame, bg="#3498db")
        name_frame.pack(fill=tk.X, pady=10)
        
        name_label = tk.Label(
            name_frame,
            text="Course Name:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        name_label.pack(side=tk.LEFT)
        
        name_value = tk.Label(
            name_frame,
            text=self.subject.get_name(),
            font=("Arial", 12),
            bg="#3498db"
        )
        name_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Rating
        rating_frame = tk.Frame(content_frame, bg="#3498db")
        rating_frame.pack(fill=tk.X, pady=10)
        
        rating_label = tk.Label(
            rating_frame,
            text="Rating:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        rating_label.pack(side=tk.LEFT)
        
        rating_value = tk.Label(
            rating_frame,
            text=f"{self.subject.get_rating()}/5.0",
            font=("Arial", 12),
            bg="#3498db"
        )
        rating_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Difficulty
        diff_frame = tk.Frame(content_frame, bg="#3498db")
        diff_frame.pack(fill=tk.X, pady=10)
        
        diff_label = tk.Label(
            diff_frame,
            text="Difficulty:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        diff_label.pack(side=tk.LEFT)
        
        diff_value = tk.Label(
            diff_frame,
            text=self.subject.get_difficulty(),
            font=("Arial", 12),
            bg="#3498db"
        )
        diff_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Your Mark
        mark_frame = tk.Frame(content_frame, bg="#3498db")
        mark_frame.pack(fill=tk.X, pady=10)
        
        mark_label = tk.Label(
            mark_frame,
            text="Your Mark:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        mark_label.pack(side=tk.LEFT)
        
        mark_value = tk.Label(
            mark_frame,
            text=f"{self.subject.mark} ({Subject.mark_to_grade(self.subject.mark)})",
            font=("Arial", 12),
            bg="#3498db"
        )
        mark_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Skills
        skills_frame = tk.Frame(content_frame, bg="#3498db")
        skills_frame.pack(fill=tk.X, pady=10)
        
        skills_label = tk.Label(
            skills_frame,
            text="Skills:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            width=15,
            anchor="w"
        )
        skills_label.pack(side=tk.LEFT, anchor="nw")
        
        skills_value = tk.Label(
            skills_frame,
            text=self.subject.get_skills(),
            font=("Arial", 12),
            bg="#3498db",
            justify=tk.LEFT,
            wraplength=400
        )
        skills_value.pack(side=tk.LEFT, fill=tk.X)
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text="Description:",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            anchor="w"
        )

        desc_label.pack(fill=tk.X, pady=(10, 5))
        
        # Create Text widget using the pattern in your code snippet
        desc_text = tk.Text(
            content_frame,
            font=("Arial", 12),
            bg="white",
            fg="black",
            height=6,
            wrap=tk.WORD
        )
        
        # Insert the description text
        desc_text.insert(tk.END, self.subject.get_description())
        
        # Make it read-only
        desc_text.config(state=tk.DISABLED)
        
        # Pack the text widget to fill and expand
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to description
        scrollbar = ttk.Scrollbar(desc_text, orient=tk.VERTICAL, command=desc_text.yview)
        desc_text.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        
        # Close button
        close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy,
            style="WhiteBorder.TButton",
            width=15
        )
        close_button.pack(pady=15)