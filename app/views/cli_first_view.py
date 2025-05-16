import questionary
from rich import print as rprint
import pandas as pd
import ast

from app.constants import USER_CSV_FILE,USER_DATA_FILE,STUDENT_ID_COL_NAME,ADM_CSV_FILE,ADM_ID_COL_NAME,COURSES_FILE,STUDENT_COURSE
from app.constants import MENU
from app.constants import ADMIN_MENU,ADMIN_OPERATION

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

def show_subjects():
    try:
        df = pd.read_csv(COURSES_FILE)

        if 'Subject_ID' not in df.columns:
            print("Error: 'Subject_ID' column not found.")
            return None

        # Convert Subject_ID column to a list of choices
        subject_ids = df['Subject_ID'].dropna().astype(str).tolist()

        if not subject_ids:
            print("No Subject IDs found in the file.")
            return None

        # Ask user to select one
        selected = questionary.select(
            "Select a Subject ID:",
            choices=subject_ids,
            use_shortcuts=False,
            style=questionary.Style([
                ("answer", "fg:#61afef"),
                ("question", "bold"),
                ("instruction", "fg:#98c379"),
            ])
        ).ask()

        return selected

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def print_students(course_id):
    try:
        mapping_df = pd.read_csv(STUDENT_COURSE)
        students_df = pd.read_csv(USER_CSV_FILE, dtype={STUDENT_ID_COL_NAME: str})

        # Check for required columns in the mapping file
        if 'StudentID' not in mapping_df.columns or 'Subjects' not in mapping_df.columns:
            print("Mapping file is missing required columns: 'StudentID', 'Subjects'.")
            return []

        # Check for required columns in the students file
        if 'StudentID' not in students_df.columns or 'FirstName' not in students_df.columns or 'LastName' not in students_df.columns:
            print("Student file is missing required columns.")
            return []

        enrolled_students = []

        # Iterate over each row in the mapping file
        for _, row in mapping_df.iterrows():
            student_id = str(row['StudentID']).strip()
            subjects_raw = row['Subjects']

            try:
                # Convert the raw subjects data into a dictionary
                subjects_dict = ast.literal_eval(subjects_raw)

                #print(subjects_dict)

                normalized_course_id = course_id.strip().upper()
                normalized_subjects_dict = {k.strip().upper(): v for k, v in subjects_dict.items()}
                #print(normalized_course_id)
                print(f"Checking student {student_id}: {normalized_subjects_dict}")
                print(f"Course ID: {normalized_course_id}, In dict: {normalized_course_id in normalized_subjects_dict}")

                if normalized_course_id in normalized_subjects_dict:
                    print("HELLO IM IN")
                # Check if the course_id is present in the subjects dictionary
                #if course_id in subjects_dict:
                    # Lookup student name in the students dataframe
                    student_info = students_df[students_df['StudentID'] == student_id]
                    print(f"Student info for {student_id}: {'Found' if not student_info.empty else 'Not found'}")  # Debug
                    if not student_info.empty:
                        print("HELLO IM OUT ")
                        first_name = student_info.iloc[0]['FirstName']
                        last_name = student_info.iloc[0]['LastName']
                        enrolled_students.append((student_id, f"{first_name} {last_name}"))
                    else:
                        print(f"Student {student_id} not found in {USER_CSV_FILE}")
                else:
                    print(f"Course {normalized_course_id} not found in subjects for student {student_id}")
            except Exception as e:
                print(f"Error processing student {student_id}: {e}")

        return enrolled_students

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []

def ask_admin_action():
    rprint("""
        [bold magenta]

         █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗        ██████╗  █████╗  ██████╗ ███████╗
        ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║        ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
        ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║        ██████╔╝███████║██║  ███╗█████╗  
        ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║        ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
        ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║        ██║     ██║  ██║╚██████╔╝███████╗
        ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                        
        """)

 
    options = [
        questionary.Choice(ADMIN_MENU.LOGIN, description="Sign in with your existing credentials", value=ADMIN_MENU.LOGIN),
        questionary.Choice(ADMIN_MENU.CANCEL, value=ADMIN_MENU.CANCEL),
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


def admin_operations():
    options = [
        questionary.Choice(ADMIN_OPERATION.SEARCH_ID, description="To Serach he Student by ID", value=ADMIN_OPERATION.SEARCH_ID),
        questionary.Choice(ADMIN_OPERATION.SEARCH_Name, description="To Serach he Student by Name", value=ADMIN_OPERATION.SEARCH_Name),
        questionary.Choice(ADMIN_OPERATION.EXPORT_REPORT,description="To EXPORT REPORT", value=ADMIN_OPERATION.EXPORT_REPORT),
        questionary.Choice(ADMIN_OPERATION.FILTER,description="To FILTER", value=ADMIN_OPERATION.FILTER),
        questionary.Choice(ADMIN_OPERATION.SEND_EMAIL,description="To SEND MAIL", value=ADMIN_OPERATION.SEND_EMAIL),
        questionary.Choice(ADMIN_OPERATION.SHOW_LOGIN_STATS,description="To SHOW LOGIN STATS", value=ADMIN_OPERATION.SHOW_LOGIN_STATS),
        questionary.Choice(ADMIN_OPERATION.LOGOUT,description="To LOGOUT", value=ADMIN_OPERATION.LOGOUT),


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


def get_student_log_data(id):
    df=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
    condition = pd.Series(True, index=df.index)
    if id is not None:
        if not id:
            raise ValueError("ID cannot be empty if provided.")
        condition &= (df['StudentID'] == id)
    matches = df[condition]
    if matches.empty:
        # print(f"No matches found for name={name}, id={id}")  # Debug    
        return False
    
    if len(matches) > 1:
            print(f"Multiple matches found: {matches[['StudentID', 'FirstName', 'LastName', 'Email']].to_dict('records')}")  # Debug
            raise ValueError("Multiple students found with the provided name. Please refine the search.")
    
    return {
            'LastLoggedIn': matches.iloc[0]['LastLoggedIn'],
            'Number_of_Logins': matches.iloc[0]['Number_of_logins'],
        }
    

                



# USE TO SEARCH THE NAME OF THE STUDENT AND SHOW THE PROFILE OF THE STUDENT..
def search_student_name(name= None, id=None):
    if name is None and id is None:
        raise ValueError("At least one search criterion (name or ID) must be provided.")
    try:
        df=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
        condition = pd.Series(True, index=df.index)
        if name is not None:
            print(name)
            name = name.lower().strip()
            if not name:
                raise ValueError("Name cannot be empty if provided.")
            condition &= (
                df['FirstName'].str.lower().str.contains(name, na=False) |
                df['LastName'].str.lower().str.contains(name, na=False)
            )
        # Add ID condition if provided
        if id is not None:
            if not id:
                raise ValueError("ID cannot be empty if provided.")
            condition &= (df['StudentID'] == id)
        # Apply filter
        matches = df[condition]
        if matches.empty:
            print(f"No matches found for name={name}, id={id}")  # Debug    
            return False
        if len(matches) > 1:
            print(f"Multiple matches found: {matches[['StudentID', 'FirstName', 'LastName', 'Email']].to_dict('records')}")  # Debug
            raise ValueError("Multiple students found with the provided name. Please refine the search.")
        # Return email and password of the first (and only) match
        return {
            'StudentID':matches.iloc[0]['StudentID'],
            'Email': matches.iloc[0]['Email'],
            'Password': matches.iloc[0]['Password'],
            'FirstName': matches.iloc[0]['FirstName'],
            'LastName': matches.iloc[0]['LastName'],
        }
    except FileNotFoundError:
        print(f"Error: {USER_CSV_FILE} not found.")  # Debug
        return False
    except Exception as e:
        print(f"Error searching students: {e}")
        return False