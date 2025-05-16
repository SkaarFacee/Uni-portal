import pytest
import pandas as pd
import os
from app.models.auth import Validate, Authentication
from app.constants import USER_CSV_FILE, USER_DATA_FILE

TEST_USERS = pd.DataFrame([
    {
        "StudentID": "S001",
        "Email": "john@university.com",
        "Password": "Abcde123",
        "FirstName": "John",
        "LastName": "Doe"
    },
    {
        "StudentID": "S002",
        "Email": "jane@university.com",
        "Password": "Xyzab999",
        "FirstName": "Jane",
        "LastName": "Smith"
    }
])

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    TEST_USERS.to_csv(USER_CSV_FILE, index=False)
    yield
    if os.path.exists(USER_CSV_FILE):
        os.remove(USER_CSV_FILE)
    if os.path.exists(USER_DATA_FILE):
        os.remove(USER_DATA_FILE)


def test_validate_password():
    assert Validate.validate_password("Abcde123") == True
    assert Validate.validate_password("abcde123") == False  
    assert Validate.validate_password("Aabc1") == False      


def test_validate_email():
    assert Validate.validate_email("john@university.com") == True
    assert Validate.validate_email("john@gmail.com") == False
    assert Validate.validate_email("john@@university.com") == False


def test_check_email_exist():
    assert Validate.check_email_exist("john@university.com") == True
    assert Validate.check_email_exist("nonexistent@university.com") == False


def test_validate_credentials():
    auth = Authentication()
    assert auth.validate_credentials("john@university.com", "Abcde123") == True
    assert auth.validate_credentials("jane@university.com", "wrongpass") == False
    assert auth.validate_credentials("nonexistent@university.com", "pass") == False
