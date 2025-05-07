import questionary
from rich import print as rprint

from app.constants import MENU
def first_user_easter_egg():
    rprint("[bold green]👋 Welcome![/bold green] [cyan]You are the first to use the system.[/cyan]")
    rprint("[bold yellow]Please register to continue.[/bold yellow] ✍️")

def ask_user():
    rprint("""
        [bold blue]
        ███╗   ███╗███████╗███╗   ██╗██╗   ██╗    ██████╗  █████╗  ██████╗ ███████╗
        ████╗ ████║██╔════╝████╗  ██║██║   ██║    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
        ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║    ██████╔╝███████║██║  ███╗█████╗  
        ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
        ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝    ██║     ██║  ██║╚██████╔╝███████╗
        ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

        [/bold blue]
        """)
    available_responses=[{'user':'Student','short_explanation':"Credentials will be your student email and pwd"},
                         {'user':'Admin','short_explanation':"Credentials will be your admin email and pwd"}]
    options = [
        questionary.Choice(cmd['user'], description=cmd['short_explanation'], value=cmd['user']) for cmd in available_responses
    ]
    options.append(questionary.Choice("Cancel"))
    options.append(questionary.Separator())
    selected = questionary.select(
            "Select command:",
            choices=options,
            use_shortcuts=True,
            style=questionary.Style(
                [
                    ("answer", "fg:#61afef"),
                    ("question", "bold"),
                    ("instruction", "fg:#98c379"),
                ]
            ),
        ).ask()
    return selected

def ask_action():   
    rprint("""
        [bold cyan]

        ███████╗████████╗██╗   ██╗██████╗ ███████╗███╗   ██╗████████╗    ██████╗  █████╗  ██████╗ ███████╗
        ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝████╗  ██║╚══██╔══╝    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
        ███████╗   ██║   ██║   ██║██║  ██║█████╗  ██╔██╗ ██║   ██║       ██████╔╝███████║██║  ███╗█████╗  
        ╚════██║   ██║   ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║   ██║       ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
        ███████║   ██║   ╚██████╔╝██████╔╝███████╗██║ ╚████║   ██║       ██║     ██║  ██║╚██████╔╝███████╗
        ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                                        
        """) 
    options = [
        questionary.Choice(MENU.LOGIN, description="Sign in with your existing credentials", value=MENU.LOGIN),
        questionary.Choice(MENU.REGISTER, description="Create a new account", value=MENU.REGISTER),
        questionary.Choice(MENU.CANCEL, value=MENU.CANCEL),
        questionary.Separator()
    ]

    selected = questionary.select(
        "What would you like to do?",
        choices=options,
        use_shortcuts=True,
        style=questionary.Style(
            [
                ("answer", "fg:#61afef"),
                ("question", "bold"),
                ("instruction", "fg:#98c379"),
            ]
        ),
    ).ask()

    return selected

def register_info(): 
    email = questionary.text("Enter your email:").ask()
    password = questionary.password("Enter your password:").ask()
    first_name = questionary.text("Enter your first name:").ask()
    last_name = questionary.text("Enter your last name:").ask()
    return {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }


