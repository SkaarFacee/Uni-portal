from rich import print as rprint
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.align import Align
import questionary

from app.constants import LANDING_MSGS,MENU

class LandingView():
    @staticmethod
    def ask_student_view():
        choice = questionary.select(
            "Choose an option:",
            choices=[
                questionary.Choice("📚 Go to Enrollments Page", value=LANDING_MSGS.ENROLLMENTS),
                questionary.Choice("👤 View Profile", value=LANDING_MSGS.PROFILE),
                questionary.Choice("Log Out", value=LANDING_MSGS.LOG_OUT),

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
    
    @staticmethod
    def successful_logout():
        rprint("\n[green]✅ You have been successfully logged out.[/green]")
        rprint()

    @staticmethod
    def enrollment_landing():
        rprint("""
            [bold cyan]
            ███████╗███╗   ██╗██████╗  ██████╗ ██╗     ██╗     ███╗   ███╗███████╗███╗   ██╗████████╗
            ██╔════╝████╗  ██║██╔══██╗██╔═══██╗██║     ██║     ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
            █████╗  ██╔██╗ ██║██████╔╝██║   ██║██║     ██║     ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   
            ██╔══╝  ██║╚██╗██║██╔══██╗██║   ██║██║     ██║     ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   
            ███████╗██║ ╚████║██║  ██║╚██████╔╝███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   
            ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                                                                                
            """)
        
    @staticmethod
    def enrollment_pending():
        rprint("[bold red]⚠️ WARNING: You have not completed enrollment![/bold red]")
        rprint()

    @staticmethod
    def enrollment_reached():
        rprint("[bold green]✅ You have completed enrollment.[/bold green]")
        rprint()

    @staticmethod
    def ask_enrollment_action():
        rprint("[green]Please choose an action below:[/green]")

        choice = questionary.select(
            "➡️ What would you like to do?",
            choices=[
                questionary.Choice("View Enrollments", value=LANDING_MSGS.VIEW_ENROLL),
                questionary.Choice("Add Enrollment", value=LANDING_MSGS.ADD_ENROLL),
                questionary.Choice("Subject details", value=LANDING_MSGS.SUBJECT_INFO),
                questionary.Choice("Go Back", value=LANDING_MSGS.BACK)
            ],
            style=questionary.Style(
                [
                    ("answer", "fg:#61afef"),
                    ("question", "bold"),
                    ("instruction", "fg:#98c379"),
                ]
            )
        ).ask()

        return choice
    
    @staticmethod
    def show_enrollments(enroll_count):
        rprint(f"[bold cyan]📊 The number of enrollments is:[/bold cyan] [bold green]{enroll_count}[/bold green]")

    @staticmethod
    def ask_subject_selection(enrollments):
        selected_subjects = questionary.checkbox(
            "✅ Select subject IDs:",
            choices=list(enrollments.keys()),
            validate=lambda selected: True if selected else "You must select at least one subject.",
        ).ask()

        return selected_subjects

    @staticmethod
    def display_student_marks(student_marks: dict):
        table = Table(title="📊 Subject Grades", style="bold cyan")

        table.add_column("Subject Code", justify="center", style="bold white")
        table.add_column("Mark", justify="center", style="bold green")
        table.add_column("Grade", justify="center", style="bold yellow")

        for subject, (mark, grade) in student_marks.items():
            table.add_row(subject, str(mark), grade)

        rprint(table)


    @staticmethod
    def display_subject_details(subjects):
        for s in subjects:
            subject_info = f"""
    [bold]Name:[/bold] {s.get_name()}
    [bold]Rating:[/bold] {s.get_rating()}
    [bold]Difficulty:[/bold] {s.get_difficulty()}
    [bold]Skills:[/bold] {s.get_skills()}
    [bold]Description:[/bold] {s.get_description()}
            """
            panel = Panel.fit(subject_info.strip(), title=f"[cyan]{s.get_name()}[/cyan]", border_style="green")
            rprint(panel)

    @staticmethod
    def ask_remove_subject():
        choice = questionary.select(
            "Do you want to remove the selected subjects. :",
            choices=[
                questionary.Choice("Yes", description='You will delete the subjects',value=True),
                questionary.Choice("No", description='This will view the subject information instead',value=False),

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
    
    @staticmethod
    def remove_success():
        rprint('[green] Successfully removed the subjects')
    
    @staticmethod
    def display_profile(student_row):
        title_text="""[bold cyan]
        ██████╗ ██████╗  ██████╗ ███████╗██╗██╗     ███████╗    ██████╗  █████╗  ██████╗ ███████╗
        ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║██║     ██╔════╝    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
        ██████╔╝██████╔╝██║   ██║█████╗  ██║██║     █████╗      ██████╔╝███████║██║  ███╗█████╗  
        ██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║     ██╔══╝      ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
        ██║     ██║  ██║╚██████╔╝██║     ██║███████╗███████╗    ██║     ██║  ██║╚██████╔╝███████╗
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                                


        """
        rprint(Align.center(title_text))
        content = f"""
        [bold cyan]Student ID     :[/bold cyan] {student_row['StudentID'].values[0]}
        [bold cyan]Email          :[/bold cyan] {student_row['Email'].values[0]}
        [bold cyan]Password       :[/bold cyan] {student_row['Password'].values[0]}
        [bold cyan]First Name     :[/bold cyan] {student_row['FirstName'].values[0]}
        [bold cyan]Last Name      :[/bold cyan] {student_row['LastName'].values[0]}
        """.strip()
        panel = Panel.fit(
            content,
            border_style="cyan",
            padding=(1, 4),
        )

        centered_panel = Align.center(panel)

        rprint(centered_panel)

    @staticmethod
    def get_subject_from_df(df):
        subject_id=[]
        rprint()
        rprint()
        rprint()
        rprint('[red] PICK A COURSE FROM THIS LIST')
        table = Table(title="Courses Table")
        [table.add_column(col, style="bold") for col in df.columns if col != 'Course Description']
        for _, row in df.iterrows():
            table.add_row(
                str(row['Subject_ID']),
                str(row['Course Name']),
                str(row['Difficulty Level']),
                str(row['Course Rating']),
                str(row['Skills'])
            )
        rprint(table)
        options = [
            questionary.Choice(
                title=row['Course Name'],  
                description=row['Skills'],
                value=row['Subject_ID']
            )
            for _, row in df.iterrows()
            ]
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
        subject_id.append(selected)

        return subject_id

    @staticmethod
    def confirm():
        choice = questionary.select(
            "Do you want to view the course choices or go back:",
            choices=[
                questionary.Choice("Yes", description='You can pick one like the same saw as below before',value=True),
                questionary.Choice("No", description='You will be taken to the previous menu',value=False),

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

    @staticmethod
    def ask_random_enroll():
        choice = questionary.select(
            "Do you want to randomly enroll :",
            choices=[
                questionary.Choice("Yes", description='You will be enrolled randomly',value=True),
                questionary.Choice("No", description='You will be asked to pick a subject',value=False),

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