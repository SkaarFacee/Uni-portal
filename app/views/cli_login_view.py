import questionary
from rich import print as rprint
class LoginView:
    @staticmethod
    def ask_username_password():
        rprint("[red]⚠️ Please make sure to use your correct email and password.[/red]\n")
        email = questionary.text("Enter your email:").ask()
        password = questionary.password("Enter your password:").ask()
        return {
            "email": email,
            "password": password
        }
    
    @staticmethod
    def ask_password():
        rprint("[cyan]🔒 Please confirm your password:[/cyan]")
        password = questionary.password("Enter password again:").ask()
        return password


    @staticmethod
    def ask_email_retry():
        rprint("[red]❌ The email you entered is invalid.[/red]")
        email = questionary.text("Please enter your email again:").ask()
        return email
    
