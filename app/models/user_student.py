from app.models.auth import Authentication,Validate
from app.models.user import User
from app.constants import MGS
from rich import print as rprint

class Student(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.auth_obj=Authentication(user_type=2)
        self.logged_in = False

    def check_if_logged_in(self):
        return True if self.logged_in else False
        
    def login(self,password=None):
        usertype = 2
        self.auth_obj.login_attempts+=1

        if Validate.check_email_exist(self.email,usertype):
            if password is not None:
                self.password=password
            if self.auth_obj.login_attempts<=3:
                if self.auth_obj.validate_credentials(self.email,self.password):
                    self.student_id=self.auth_obj.get_student_id(self.email,usertype)
                    self.logged_in=True
                    return True
                else :
                    rprint(f"[yellow]🔁 Try Again:[/yellow] ([bold red]{self.auth_obj.login_attempts}[/bold red]/5) attempts used")
                    return MGS.TRY_PASSWORD_AGAIN
            if self.auth_obj.login_attempts>3:
                return False
        else:
            return None
        
    def change_password(self,new_password):
        if self.auth_obj.check_old_password_equals_new(self.password,new_password):
            print("Enter a password different from the old password")
        else:
            if Validate.validate_password(new_password):
                self.auth_obj.reset_password(self.email,new_password)
                self.password=new_password

    def logout(self):
        self.logged_in=False
        return True
    