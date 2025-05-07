import time
import os 
from rich import print as rprint
import questionary


class Loading:
    @staticmethod
    def init_loading(console):
        with console.status("[bold blue]Setting all the backend up.", spinner="dots"):
            time.sleep(2)
    

    @staticmethod
    def max_attemps(console):
        with console.status("[bold red]⏳ Max attempts reached. Please wait 10 seconds before trying again...[/bold red]", spinner="dots"):
            time.sleep(10)
            
    @staticmethod
    def menu_or_exit():
        rprint("\n[cyan]🔁 Would you like to return to the login menu or exit?[/cyan]")

        choice = questionary.select(
            "Choose an option:",
            choices=[
                questionary.Choice("🔐 Return to Login Menu", value=True),
                questionary.Choice("❌ Exit", value=False)
            ],
            style=questionary.Style(
                [
                    ("answer", "fg:#61afef"),
                    ("question", "bold"),
                    ("instruction", "fg:#98c379"),
                ]
            ),
        ).ask()

        return choice