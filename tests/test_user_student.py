import pytest
from unittest.mock import patch, MagicMock
from app.models.user_student import Student
import os
@pytest.fixture
def student():
    return Student("test@university.com", "OldPass12345")


def test_check_if_logged_in_false(student):
    assert student.check_if_logged_in() is False


@patch("app.models.user_student.Validate.check_email_exist", return_value=True)
@patch("app.models.user_student.Authentication.validate_credentials", return_value=False)
def test_login_fail_then_lockout(mock_validate_credentials, mock_check_email_exist, student):
    student.auth_obj.login_attempts = 3
    result = student.login()
    assert result is False


@patch("app.models.user_student.Validate.check_email_exist", return_value=False)
def test_login_email_does_not_exist(mock_check_email_exist, student, capsys):
    result = student.login()
    captured = capsys.readouterr()
    assert result is None


@patch("app.models.user_student.Validate.validate_password", return_value=True)
@patch("app.models.user_student.Authentication.reset_password")
@patch("app.models.user_student.Authentication.check_old_password_equals_new", return_value=False)
def test_change_password_success(mock_check_old, mock_reset_password, mock_validate_password, student):
    student.change_password("NewPass123!")
    # mock_reset_password.assert_called_once_with("test@example.com", "NewPass123!")
    assert student.password == "NewPass123!"


@patch("app.models.user_student.Authentication.check_old_password_equals_new", return_value=True)
def test_change_password_same_as_old(mock_check_old, student, capsys):
    student.change_password("OldPass123!")
    captured = capsys.readouterr()
    assert "Enter a password different from the old password" in captured.out


def test_logout_sets_logged_in_false(student):
    student.logged_in = True
    result = student.logout()
    assert result is True
    assert student.logged_in is False
