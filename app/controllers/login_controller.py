# Code for logging in 
from app.models.user_student import Student,Admin
from app.constants import ERRORS,MGS

from app.views.cli_loading import Loading
from app.views.cli_login_view import LoginView

from app.utils import console

class LoginController():

    def __init__(self,email,password):
        self.user=Student(email,password)

    def login(self):
        result = self.user.login()
        while True:
            if result is True:
                return True

            if result == MGS.TRY_PASSWORD_AGAIN or result is False:
                if result is False:
                    Loading.max_attemps(console)
                    self.user.auth_obj.login_attempts = 0
                result = self.user.login(LoginView.ask_password())

            else:
                self.user.email = LoginView.ask_email_retry()
                result = self.user.login(LoginView.ask_password())
    def get_user(self):
        return self.user
    
    def log_out(self):
        self.user.logout()
        return True

class AdminLoginController():
    def __init__(self, email, password):
        self.user = Admin(email, password)

    def login(self):
        result = self.user.login()
        while True:
            if result is True:
                return True
            if result == MGS.TRY_PASSWORD_AGAIN or result is False:
                if result is False:
                    Loading.max_attemps(console)
                    self.user.auth_obj.login_attempts = 0
                result = self.user.login(LoginView.ask_password())
            else:
                self.user.email = LoginView.ask_email_retry()
                result = self.user.login(LoginView.ask_password())

    def get_user(self):
        return self.user
