from rich import print as rprint

class RegisterView:
    def show_invalid_email_message(self):
        rprint("[bold red]❌ Invalid Email![/bold red]")
        rprint("[yellow]Emails should end with the domain[/yellow] [bold blue]@university.com[/bold blue] :email:")

    def show_invalid_password_message(self):
        rprint("[bold red]❌ Invalid password![/bold red] Please ensure it meets the following criteria:\n")
        rprint(
            "[bold yellow]-[/bold yellow] It starts with an [bold]upper-case letter[/bold]\n"
            "[bold yellow]-[/bold yellow] It contains at least [bold]five (5) letters[/bold]\n"
            "[bold yellow]-[/bold yellow] It is followed by [bold]three (3) or more digits[/bold]"
        )
    def show_email_exists_message(self):
        rprint("[bold red]⚠️ The email you entered already exists.[/bold red]")
        rprint("[yellow]Please try logging in or use a different email to register.[/yellow]")
    @staticmethod
    def register_success():
        rprint("[bold green]✅ Registration successful![/bold green]")

