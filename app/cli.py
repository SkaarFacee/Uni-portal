import sys


import dotenv
import pyperclip
import questionary
from rich import print as rprint
from rich.console import Console


from views.cli_loading import Loading
from controllers.loaders import change_dir
from utils import console
change_dir()
Loading.init_loading(console)


from app.views.cli_first_view import ask_user,ask_action

from app.controllers.register import RegisterController,RegistrationLoopController
from app.views.cli_first_view import register_info
from app.constants import MENU,MGS,ERRORS,LANDING_MSGS
from app.views.cli_register_view import RegisterView
from app.views.cli_login_view import LoginView
from app.views.cli_landing_view import LandingView

from app.controllers.login_controller import LoginController
from app.controllers.enrollment_controller import EnrollmentController

def registration_app():
    while True:
        registration_data = register_info()
        valid_message = RegisterController.register_student(rego_obj, registration_data)
        if valid_message==True:
            RegisterView.register_success()
            login_info=LoginView.ask_username_password()
            break
        else:
            RegistrationLoopController().registration_error_printer(valid_message) 


if __name__ == "__main__":
    user_type=ask_user()
    if user_type=='Student':
        rego_obj=RegisterController.pre_registration()
        while True:
            match ask_action():
                case MENU.LOGIN:
                    login_info=LoginView.ask_username_password()
                    login_obj=LoginController(**login_info)
                    login_response=login_obj.login()
                    if login_response: 
                        enroll_ment_obj=EnrollmentController(login_obj.get_user())
                        while login_obj.user.logged_in:
                            student_choice=enroll_ment_obj.menu_choice()
                            match student_choice:
                                case LANDING_MSGS.LOG_OUT:
                                    login_obj.log_out()
                                    LandingView.successful_logout()
                                case LANDING_MSGS.PROFILE:
                                    enroll_ment_obj.profile_menu()
                                case LANDING_MSGS.ENROLLMENTS:
                                    enroll_ment_obj.enroll_menu()
                        


                case MENU.REGISTER:
                    registration_app()
                case MENU.CANCEL:
                    print("Operation cancelled.")
                    sys.exit()
            print('GOING BACK TO MENU LOADING SCREEN')






# email='Aditya8anil@university.com'
# password='HelloWorld12345'
# first_name='Aditya'
# last_name="Anil"
# if all((Validate.validate_email(email),Validate.validate_password(password),not Validate.check_email_exist(email))):
#     print('User registered')
#     rego_obj.register_student(email,password,first_name,last_name)
# else: 
#     print('User not created')

