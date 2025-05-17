from app.models.user_admin import Admin
from app.constants import ERRORS,MGS
from app.controllers.login_controller import LoginController
from app.views.cli_loading import Loading
from app.views.cli_login_view import LoginView

from app.utils import console

import pandas as pd 
class AdminLoginController(LoginController):
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
    
    def get_all_students(self):
        return self.user.get_all_students()

    def categorize_by_grade(self):
        return self.user.categorize_by_grade()
    
    def categorize_by_p_or_f(self):
        return self.user.categorize_pass_fail()
    
    def delele_student_id(self,id):
        return self.user.remove_student(id)
    
    def delete_all_student_data(self):
        return self.user.delete_all_students()
    
    def report_creater(self):
        self.user.export_student_report()

    def backup(self):
        return self.user.backup_all_student_files()
    
    def restore(self):
        return self.user.restore_all_student_files()