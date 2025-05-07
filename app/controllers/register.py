from app.models.student_registration import Registration
from app.models.auth import Validate
from app.views.cli_first_view import register_info,first_user_easter_egg
from app.constants import ERRORS
from app.views.cli_register_view import RegisterView
class RegisterController:
    @staticmethod
    def pre_registration():
        rego_obj=Registration()
        if rego_obj.file_created:
            first_user_easter_egg() 
        return rego_obj
    @staticmethod
    def register_student(rego_obj,input_info):
        if not Validate.validate_email(input_info['email']):
            return ERRORS.EMAIL_VALIDATION_ERROR
        if not Validate.validate_password(input_info['password']):
            return ERRORS.PASSWORD_VALIDATION_ERROR
        if Validate.check_email_exist(input_info['email']):
            return ERRORS.USER_ALREDY_EXISTS_ERROR
        else:
            rego_obj.register_student(**input_info)
            return True
        
class RegistrationLoopController:
    def __init__(self):
        self.error_printer=RegisterView()

    def registration_error_printer(self,error_type):
        match error_type:
            case ERRORS.EMAIL_VALIDATION_ERROR:
                self.error_printer.show_invalid_email_message()
            case ERRORS.PASSWORD_VALIDATION_ERROR:
                self.error_printer.show_invalid_password_message()
            case ERRORS.USER_ALREDY_EXISTS_ERROR:
                self.error_printer.show_email_exists_message()





