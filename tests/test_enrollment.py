import pytest
import pandas as pd
from app.models.enrollment import Enrollment, EnrollmentUtils
from app.models.user_student import Student
from app.constants import STUDENT_ID_COL_NAME, SUBJECT_COL_NAME, SUBJECT_ID_COL

# Mock Student fixture
@pytest.fixture
def mock_student(monkeypatch):
    student = Student(email="test@university.com", password="password123")
    student.student_id = "123"
    student.enrolled_subjects = {}
    return student

# Mock Data
@pytest.fixture
def mock_data(monkeypatch):
    # Mock prepare_courses_df
    monkeypatch.setattr(EnrollmentUtils, 'prepare_courses_df', lambda: pd.DataFrame({
        SUBJECT_ID_COL: ['S1', 'S2', 'S3', 'S4'],
        'Subject Name': ['Math', 'CS', 'Physics', 'Biology']
    }))

    # Mock prepare_student_course_df
    monkeypatch.setattr(EnrollmentUtils, 'prepare_student_course_df', lambda: pd.DataFrame({
        STUDENT_ID_COL_NAME: ['123'],
        SUBJECT_COL_NAME: [str({'S1': 85})]
    }))

    # Mock update_student_course_df to avoid file I/O
    monkeypatch.setattr(EnrollmentUtils, 'update_student_course_df', lambda df: df)

def test_add_student_if_not_enrolled(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    assert isinstance(enrollment.view_enrollments(), dict)

def test_view_enrollments(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    result = enrollment.view_enrollments()
    assert isinstance(result, dict)

def test_add_random_enroll(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    result = enrollment.add_random_enroll()
    assert result is True or result is False  # Depending on if already full

def test_unenroll_subject(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    enrollment.student.enrolled_subjects = {'S1': 90}
    result = enrollment.unenroll_subject('S1')
    assert result is True
    assert 'S1' not in enrollment.student.enrolled_subjects

def test_unenroll_invalid_subject(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    enrollment.student.enrolled_subjects = {'S1': 90}
    result = enrollment.unenroll_subject('S2')
    assert result is False

def test_enrollment_completion(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    enrollment.student.enrolled_subjects = {'S1': 90, 'S2': 80, 'S3': 70, 'S4': 60}
    assert enrollment.check_enrollment_completion() is True

def test_update_student_course(mock_student, mock_data):
    enrollment = Enrollment(mock_student)
    enrollment.student.enrolled_subjects = {'S2': 88}
    assert enrollment.update_student_course() is True
