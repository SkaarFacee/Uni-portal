import questionary
from rich import print as rprint
from rich.table import Table
import pandas as pd
import ast

from app.constants import ADMIN_MENU,ADMIN_OPERATION,USER_CSV_FILE,STUDENT_ID_COL_NAME,COURSES_FILE,STUDENT_COURSE


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
        questionary.Choice(' '.join(ADMIN_OPERATION.VIEW_ALL_STUDENTS.split('_')).title(), description="View all the students", value=ADMIN_OPERATION.VIEW_ALL_STUDENTS),
        questionary.Choice(' '.join(ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_GRADE.split('_')).title(), description="View students by their grades", value=ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_GRADE),
        questionary.Choice(' '.join(ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_PASS_FAIL.split('_')).title(), description="View students by pass and fail", value=ADMIN_OPERATION.CATEGORIZE_STUDENTS_BY_PASS_FAIL),
        questionary.Choice(' '.join(ADMIN_OPERATION.DELETE_ID.split('_')).title(), description="Delete student data by ID", value=ADMIN_OPERATION.DELETE_ID),
        questionary.Choice(' '.join(ADMIN_OPERATION.DELETE_ALL.split('_')).title(), description="Delete all student data", value=ADMIN_OPERATION.DELETE_ALL),
        questionary.Choice(ADMIN_OPERATION.SEARCH_ID, description="To Serach he Student by ID", value=ADMIN_OPERATION.SEARCH_ID),
        questionary.Choice(ADMIN_OPERATION.SEARCH_Name, description="To Serach he Student by Name", value=ADMIN_OPERATION.SEARCH_Name),
        questionary.Choice(ADMIN_OPERATION.EXPORT_ALL_REPORT_CSV,description="To EXPORT REPORT", value=ADMIN_OPERATION.EXPORT_ALL_REPORT_CSV),
        questionary.Choice(ADMIN_OPERATION.FILTER,description="To FILTER", value=ADMIN_OPERATION.FILTER),
        questionary.Choice(ADMIN_OPERATION.SHOW_LOGIN_STATS,description="To SHOW LOGIN STATS", value=ADMIN_OPERATION.SHOW_LOGIN_STATS),
        questionary.Choice(' '.join(ADMIN_OPERATION.CREATE_BACKUP.split('_')).title(), description="Create a backup", value=ADMIN_OPERATION.CREATE_BACKUP),
        questionary.Choice(' '.join(ADMIN_OPERATION.LOAD_BACKUP.split('_')).title(), description="Restore from a latest backup", value=ADMIN_OPERATION.LOAD_BACKUP),
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

def view_all_students(df):
    table = Table(title="Student Information")

    for col in df.columns:
        table.add_column(col, style="bold cyan")

    for _, row in df.iterrows():
        table.add_row(*map(str, row))

    rprint(table)


def view_grade_summary(df):
    table = Table(title="📊 Student Grade Summary")
    headers = ["StudentID", "Z", "P", "C", "D", "HD", "TopGradeCategory"]
    for header in headers:
        table.add_column(header, style="cyan" if header != "TopGradeCategory" else "magenta", justify="center")

    for _, row in df[headers].iterrows():
        table.add_row(*[str(val) for val in row])

    rprint(table)

def view_pass_fail_table(df):
    table = Table(title="Student Course Pass/Fail Summary")

    table.add_column("StudentID", style="cyan", no_wrap=True)
    table.add_column("Passed Courses", style="green")
    table.add_column("Failed Courses", style="red")

    for _, row in df.iterrows():
        passed = ", ".join(row["PassedCourses"]) if row["PassedCourses"] else "-"
        failed = ", ".join(row["FailedCourses"]) if row["FailedCourses"] else "-"
        table.add_row(row["StudentID"], passed, failed)

    rprint(table)

def search_student_name(name= None, id=None):
    if name is None and id is None:
        raise ValueError("At least one search criterion (name or ID) must be provided.")
    try:
        df=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
        condition = pd.Series(True, index=df.index)
        if name is not None:
            name = name.lower().strip()
            if not name:
                raise ValueError("Name cannot be empty if provided.")
            condition &= (
                df['FirstName'].str.lower().str.contains(name, na=False) |
                df['LastName'].str.lower().str.contains(name, na=False)
            )
        if id is not None:
            if not id:
                raise ValueError("ID cannot be empty if provided.")
            condition &= (df['StudentID'] == id)
        matches = df[condition]
        if matches.empty:
            print(f"No matches found for name={name}, id={id}")   
            return False
        if len(matches) > 1:
            print(f"Multiple matches found: {matches[['StudentID', 'FirstName', 'LastName', 'Email']].to_dict('records')}")  # Debug
            raise ValueError("Multiple students found with the provided name. Please refine the search.")
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
                # Check if the course_id is present in the subjects dictionary
                #if course_id in subjects_dict:
                    # Lookup student name in the students dataframe
                    student_info = students_df[students_df['StudentID'] == student_id]
                    print(f"Student info for {student_id}: {'Found' if not student_info.empty else 'Not found'}")  # Debug
                    if not student_info.empty:
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
