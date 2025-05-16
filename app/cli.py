import sys
sys.stdout.reconfigure(encoding='utf-8')

import dotenv
import pyperclip
import questionary
from rich import print as rprint
from rich.console import Console
# from app.models.auth import Authentication

from views.cli_loading import Loading
from controllers.loaders import change_dir
from utils import console
change_dir()
Loading.init_loading(console)

from app.views.cli_first_view import ask_user,ask_action,ask_admin_action,admin_operations,search_student_name,show_subjects,print_students,get_student_log_data

from app.controllers.register import RegisterController,RegistrationLoopController
from app.views.cli_first_view import register_info
from app.constants import MENU,MGS,ERRORS,LANDING_MSGS,ADMIN_MENU,ADMIN_OPERATION,USER_CSV_FILE
from app.views.cli_register_view import RegisterView
from app.views.cli_login_view import LoginView
from app.views.cli_landing_view import LandingView

from app.controllers.login_controller import LoginController,AdminLoginController
from app.controllers.enrollment_controller import EnrollmentController
from app.models.auth import Authentication

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
                    #print(login_info)
                    email = login_info['email']
                    print(email)
                    login_obj=LoginController(**login_info)
                    login_response=login_obj.login()
                    if login_response:
                        enroll_ment_obj=EnrollmentController(login_obj.get_user())
                        auth_obj = Authentication(user_type=2)
                        student_id = auth_obj.get_student_id(email,usertype=2)
                        print(student_id)
                        enroll_ment_obj.update_login_info(student_id)
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
    elif user_type=='Admin':
        while True:
            match ask_admin_action():
                case ADMIN_MENU.LOGIN:
                    login_info=LoginView.ask_username_password()
                    login_obj=AdminLoginController(**login_info)
                
                    login_response=login_obj.login()
                    if login_response:
                        while True:
                            match admin_operations():
                                case ADMIN_OPERATION.SEARCH_ID:
                                    ids = input('Enter student id: ')
                                    data = search_student_name(id=ids)
                                    print(data)
                                    LandingView.display_student_data(data)
                                case ADMIN_OPERATION.SEARCH_Name:
                                    name = input('Enter student name: ')
                                    data = search_student_name(name=name)
                                    print(data)
                                    LandingView.display_student_data(data)
                                case ADMIN_OPERATION.EXPORT_REPORT:
                                    print('You export report option')
                                case ADMIN_OPERATION.FILTER:
                                    #print('You filter menu option')
                                    subject = show_subjects()
                                    students = print_students(subject)
                                    # print(students)
                                    LandingView.display_student_filtered_data(students)
                                    #print('You seleceted ',subject)
                                case ADMIN_OPERATION.SEND_EMAIL:
                                    print('You selected search option')
                                case ADMIN_OPERATION.SHOW_LOGIN_STATS:
                                    print('You export report option')
                                    student_id_log = input('Enter the Student ID: ')
                                    data = get_student_log_data(student_id_log)
                                    LandingView.display_student_loginfo_data(data)
                                case ADMIN_OPERATION.LOGOUT:
                                    print("Logging out...")
                                    break;
                case ADMIN_MENU.CANCEL:
                    print("Operation cancelled.")
                    break;
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

