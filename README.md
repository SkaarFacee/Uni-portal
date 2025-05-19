# Uni-Portal

**Uni-Portal** is a Python-based command-line and graphical interface application designed to simulate a simplified university student management system. It allows students to register, enroll in courses, view their profiles, and for administrators to perform powerful data operations, all in a secure and user-friendly environment.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Features](#features)
  - [Student Features (CLI)](#student-features-cli)
  - [Admin Features (CLI)](#admin-features-cli)
  - [GUI Application](#gui-application)
- [External Libraries](#external-libraries)
- [License](#license)

---

## Overview

Uni-Portal supports:
- Student registration and secure login
- Course enrollment and management
- Admin controls with reporting and backups
- Role-based access with CLI and GUI for student portal

---

## Prerequisites

Before getting started, ensure you have the following installed:

- [Miniconda or Anaconda](https://docs.conda.io/en/latest/miniconda.html) (used for Python environment management)
- Python 3.12+

---

## Setup Instructions

Follow these steps to set up the application:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/SkaarFacee/Uni-portal.git
    cd Uni-portal
    ```
2.  **Create a Conda environment**
    ```bash
    conda create -n uni-portal-env python=3.12
    conda activate uni-portal-env
    ```
3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Application

**Note:** Before using the GUI, ensure you run the CLI application first to register a student account. GUI features are limited to registered students.

1.  **Activate the environment**
    ```bash
    conda activate uni-portal-env
    ```
2.  **Run the CLI application**
    ```bash
    python cli.py
    ```
3.  **Run the GUI application**
    ```bash
    python gui.py
    ```

---

## Features

### Student Features (CLI)

-   **User Registration and Login**
    -   Emails must end with `@university.com`
    -   Passwords must follow these rules 
	    - Starts with one uppercase letter
	    - Is followed by at least 4 letters** (uppercase or lowercase)
	    - Ends with at least 3 digits
	    - Contains no other characters (no spaces, symbols, etc.)
    -   Login attempts are rate-limited with timeout protection
    -   Registered users receive a unique 6-digit Student ID
-   **Enrollment Management**
    -   Enroll in courses manually or select a random set of 4
    -   Courses come pre-filled with randomly assigned grades
    -   Option to unenroll from any course
    -   View details about enrolled courses
-   **Profile Viewing**
    -   Display user information, including registered details and current courses

### Admin Features (CLI)

Admin functionalities are command-driven and include:

-   **Student Overview**
    -   View all registered student accounts
    -   Categorize students by grade or pass/fail status
-   **Search & Filtering**
    -   Search students by ID or name
    -   Apply filters to target specific subsets of students
-   **Account Management**
    -   Delete a student by ID
    -   Delete all students
-   **Reporting & Backup**
    -   Export student data to CSV for offline analysis
    -   Create and load data backups
-   **Communication**
    -   Send emails to students via configured channels
-   **System Monitoring**
    -   View login statistics for audit or performance checks
    -   Secure logout functionality for session control

### GUI Application

The GUI provides a more visual experience for student users. It supports:

-   Secure login
-   Access to features like enrollment, profile viewing, and logout
-   **Note:** Registration and detailed course information views are only available via CLI.

---

## External Libraries

This project leverages several open-source Python libraries:

-   **questionary**
    -   Used to build interactive command-line prompts, making the CLI experience smooth and intuitive.
-   **rich**
    -   Enhances terminal output with styled text, tables, and progress bars. Used for clean, visually rich CLI interfaces.
-   **pandas**
    -   Powers data processing, storage, and export. Essential for managing student information, filtering, and generating reports.
-   **shutil**
    -   Standard library used for file operations like backups and copying files.
-   **tkinter**
    -   Built-in GUI library for Python, used to build the graphical version of the application for student users.
-   **ast**
    -   Parses and analyzes Python code in string form, useful for reading and manipulating config files or saved data formats.
-   **re**
    -   Regular expressions for validating email formats and passwords during user registration.
-   **pytest**
    -   Framework used for automated testing, ensuring the codebase remains reliable and maintainable.

---
