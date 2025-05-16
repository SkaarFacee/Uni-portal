import os
import pytest
import sys 


from app.models.student_registration import Registration, RegistrationUtils
from app.constants import USER_DATA_FILE


project_root = os.path.abspath(os.path.join(os.getcwd()))
os.chdir(project_root)
if project_root not in sys.path:
    sys.path.insert(0, project_root)    


@pytest.fixture()
def create_file():
    register_obj=Registration()

def test_file_creation():
    registration = Registration()
    print(registration.file_path)
    assert os.path.exists(registration.file_path)
    os.remove(registration.file_path)

def test_registration_file_status_created():
    registration = Registration()
    assert registration.registeration_file_status().startswith("✅")

def test_registration_file_status_exists():
    registration = Registration()
    assert registration.registeration_file_status().startswith("ℹ️")
    os.remove(registration.file_path)

def test_generate_student_id_initial(create_file):
    student_id = RegistrationUtils.generate_student_id()
    assert student_id == "000001"

def test_generate_student_id_increments():
    new_student=Registration().register_student("test@university.com","Pass123","Test","User")
    student_id = RegistrationUtils.generate_student_id()
    assert student_id == "000002"
    os.remove(Registration().file_path)

def test_register_student_adds_data():
    registration = Registration()
    result = registration.register_student(
        email="alice@university.com",
        password="Password123",
        first_name="Alice",
        last_name="Smith"
    )
    assert result is True

    with open(registration.file_path, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 1
    parts = lines[0].strip().split(',')
    assert parts[1] == "alice@university.com"
    assert parts[3] == "Alice"
    assert len(parts[0]) == 6  
    assert os.path.exists(registration.all_data_path)

def test_register_multiple_students_unique_ids():
    registration = Registration()
    ids = set()
    for i in range(5):
        registration.register_student(
            email=f"user{i}@university.com",
            password="Pass1234",
            first_name=f"User{i}",
            last_name="Test"
        )
        with open(registration.file_path, 'r') as f:
            last_line = f.readlines()[-1]
            student_id = last_line.strip().split(',')[0]
            assert student_id not in ids
            ids.add(student_id)

    assert len(ids) == 5
    os.remove(registration.file_path)
    os.remove(registration.all_data_path)

