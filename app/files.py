import os
import pandas as pd

# Define the paths (use the same paths defined in constants.py)
USER_DATA_FILE = 'app/models/data/students.data'
USER_CSV_FILE = 'app/models/data/complete_data.csv'
COURSES_FILE = 'app/models/data/courses.csv'
STUDENT_COURSE = 'app/models/data/student_course_mapping.csv'

# Ensure directory exists
os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)

# Create empty students.data if it doesn't exist
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        pass  # Create empty file

# Create complete_data.csv with proper headers
if not os.path.exists(USER_CSV_FILE):
    df = pd.DataFrame(columns=['StudentID', 'Email', 'Password', 'FirstName', 'LastName'])
    df.to_csv(USER_CSV_FILE, index=False)

# Create student_course_mapping.csv with proper headers
if not os.path.exists(STUDENT_COURSE):
    df = pd.DataFrame(columns=['StudentID', 'Subjects'])
    df.to_csv(STUDENT_COURSE, index=False)

# Create courses.csv with sample data if it doesn't exist
if not os.path.exists(COURSES_FILE):
    courses_data = {
        'Subject_ID': ['CS101', 'CS102', 'MATH101', 'ENG101', 'PHYS101'],
        'Course Name': ['Introduction to Programming', 'Data Structures', 'Calculus I', 'English Composition', 'Physics I'],
        'Course Description': [
            'Learn the basics of programming using Python',
            'Study fundamental data structures and algorithms',
            'Introduction to differential and integral calculus',
            'Develop effective writing and communication skills',
            'Introduction to mechanics and physics principles'
        ],
        'Course Rating': [4.5, 4.2, 3.8, 4.0, 3.7],
        'Difficulty Level': ['Beginner', 'Intermediate', 'Intermediate', 'Beginner', 'Intermediate'],
        'Skills': [
            'Python, Programming Logic, Problem Solving',
            'Algorithms, Data Structures, Programming',
            'Mathematics, Analysis, Problem Solving',
            'Writing, Communication, Critical Thinking',
            'Physics, Mathematics, Scientific Thinking'
        ]
    }
    df = pd.DataFrame(courses_data)
    df.to_csv(COURSES_FILE, index=False)
    
print("All required files have been created successfully!")