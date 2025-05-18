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

from app.views.cli_first_view import MAIN_UTILS
from app.views.cli_admin_view import ask_admin_action,admin_operations,search_student_name,show_subjects,print_students,get_student_log_data,view_all_students,view_grade_summary,view_pass_fail_table

from app.controllers.register import RegisterController,RegistrationLoopController
from app.constants import MENU,MGS,ERRORS,LANDING_MSGS,ADMIN_MENU,ADMIN_OPERATION,USER_CSV_FILE
from app.views.cli_register_view import RegisterView
from app.views.cli_login_view import LoginView
from app.views.cli_landing_view import LandingView

from app.controllers.login_controller_student import StudentLoginController
from app.controllers.login_controller_admin import AdminLoginController
from app.controllers.enrollment_controller import EnrollmentController
from app.models.auth import Authentication



def registration_app():
    while True:
        registration_data = MAIN_UTILS.register_info()
        valid_message = RegisterController.register_student(rego_obj, registration_data)
        if valid_message==True:
            RegisterView.register_success()
            break
        else:
            RegistrationLoopController().registration_error_printer(valid_message)


if __name__ == "__main__":
    user_type=MAIN_UTILS.ask_user()
    if user_type=='Student':
        rego_obj=RegisterController.pre_registration()
        while True:
            match MAIN_UTILS.ask_action():
                case MENU.LOGIN:
                    login_info=LoginView.ask_username_password()
                    email = login_info['email']
                    login_obj=StudentLoginController(**login_info)
                    login_response=login_obj.login()
                    if login_response:
                        enroll_ment_obj=EnrollmentController(login_obj.get_user())
                        auth_obj = Authentication(user_type=2)
                        student_id = auth_obj.get_student_id(email,usertype=2)
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
                    MAIN_UTILS.logout_animation()
                    sys.exit()
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
                                case ADMIN_OPERATION.VIEW_ALL_STUDENTS:
                                    students_data=login_obj.get_all_students()
                                    view_all_students(students_data)

                                case ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_GRADE:
                                    view_df=login_obj.categorize_by_grade()
                                    view_grade_summary(view_df)

                                case ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_PASS_FAIL:
                                    view_df=login_obj.categorize_by_p_or_f()
                                    view_pass_fail_table(view_df)

                                case ADMIN_OPERATION.DELETE_ID:
                                    flag=login_obj.delele_student_id(str(input('Enter studend id to be deleted')))
                                    if flag==False:
                                        print('There was some error try again')
                                
                                case ADMIN_OPERATION.DELETE_ALL:
                                    flag=login_obj.delete_all_student_data()
                                    if flag==False:
                                        print('There was some error try again')


                                case ADMIN_OPERATION.SEARCH_ID:
                                    ids = input('Enter student id: ')
                                    data = search_student_name(id=ids)
                                    LandingView.display_student_data(data)
                                case ADMIN_OPERATION.SEARCH_Name:
                                    name = input('Enter student name: ')
                                    data = search_student_name(name=name)
                                    LandingView.display_student_data(data)
                                case ADMIN_OPERATION.EXPORT_ALL_REPORT_CSV:
                                    login_obj.report_creater()
                                case ADMIN_OPERATION.FILTER:
                                    subject = show_subjects()
                                    students = print_students(subject)
                                    LandingView.display_student_filtered_data(students)
                                case ADMIN_OPERATION.CREATE_BACKUP:
                                    flag=login_obj.backup()
                                    if flag==False:
                                        print('There was some error try again')

                                case ADMIN_OPERATION.LOAD_BACKUP:
                                    flag=login_obj.restore()
                                    if flag==False:
                                        print('There was some error try again')

                                case ADMIN_OPERATION.SHOW_LOGIN_STATS:
                                    student_id_log = input('Enter the Student ID: ')
                                    data = get_student_log_data(student_id_log)
                                    LandingView.display_student_loginfo_data(data)
                                case ADMIN_OPERATION.LOGOUT:
                                    break
                case ADMIN_MENU.CANCEL:
                    MAIN_UTILS.logout_animation()
                    sys.exit()