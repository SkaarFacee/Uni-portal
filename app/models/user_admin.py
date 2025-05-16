from app.models.auth import Authentication,Validate
from app.models.user import User
from app.constants import MGS
from app.constants import USER_CSV_FILE,STUDENT_ID_COL_NAME,STUDENT_COURSE,USER_DATA_FILE

from rich import print as rprint
from datetime import datetime
import shutil
import pandas as pd 
import ast 
import os 


class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.auth_obj = Authentication(user_type=1)
        self.logged_in = False
        self.complete_data=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
        self.student_course_mapping_df=pd.read_csv(STUDENT_COURSE,dtype={STUDENT_ID_COL_NAME: str})
    def check_if_logged_in(self):
        return True if self.logged_in else False

    def login(self, password=None):
        usertype = 1
        self.auth_obj.login_attempts += 1

        if Validate.check_email_exist(self.email,usertype):
            if password is not None:
                self.password = password
            if self.auth_obj.login_attempts <= 3:
                if self.auth_obj.validate_credentials(self.email, self.password):
                    self.admin_id = self.auth_obj.get_admin_id(self.email,usertype)
                    self.logged_in = True
                    return True
                else:
                    rprint(f"[yellow]🔁 Try Again:[/yellow] ([bold red]{self.auth_obj.login_attempts}[/bold red]/3) attempts used")
                    return MGS.TRY_PASSWORD_AGAIN
            if self.auth_obj.login_attempts > 3:
                return False
        else:
            return None

    def logout(self):
        self.logged_in = False
        return True
    
    def get_all_students(self):
        return self.complete_data[[STUDENT_ID_COL_NAME,"FirstName","LastName"]]

    def merge_data(self):
        return pd.merge(self.complete_data, self.student_course_mapping_df, on="StudentID")


    def count_grades(self,subject_str):
        subject_dict = ast.literal_eval(subject_str)
        grade_categories = ["Z", "P", "C", "D", "HD"]
        grade_counts = {grade: 0 for grade in grade_categories}
        for subject_data in subject_dict.values():
            grade = subject_data[1]
            if grade in grade_counts:
                grade_counts[grade] += 1
        return pd.Series(grade_counts)
    
    def categorize_by_grade(self):
        df=self.merge_data()
    
        grade_df = df["Subjects"].apply(self.count_grades)
        df = pd.concat([df, grade_df], axis=1)

        df["TopGradeCategory"] = grade_df.idxmax(axis=1)

        return(df[["StudentID", "Z", "P", "C", "D", "HD", "TopGradeCategory"]])
    
    @staticmethod
    def get_pass_fail_courses(subject_str):
        fail_grades = {"Z"}
        pass_grades = {"P","C", "D", "HD"}
        subject_dict = ast.literal_eval(subject_str)
        passed = []
        failed = []
        for course_code, subject_data in subject_dict.items():
            grade = subject_data[1]
            if grade in pass_grades:
                passed.append(course_code)
            elif grade in fail_grades:
                failed.append(course_code)
  
        return pd.Series([passed, failed])

    def categorize_pass_fail(self):
        df = self.merge_data()
        df[["PassedCourses", "FailedCourses"]] = df["Subjects"].apply(self.get_pass_fail_courses)
        return df[["StudentID", "PassedCourses", "FailedCourses"]]
    
    

    def remove_student(self, student_id):
        if student_id not in self.complete_data[STUDENT_ID_COL_NAME].values:
            rprint(f"[red]❌ Student ID {student_id} not found.[/red]")
            return False
        self.complete_data = self.complete_data[self.complete_data[STUDENT_ID_COL_NAME] != student_id]
        self.student_course_mapping_df = self.student_course_mapping_df[
            self.student_course_mapping_df[STUDENT_ID_COL_NAME] != student_id
        ]
        self.complete_data.to_csv(USER_CSV_FILE, index=False)
        self.student_course_mapping_df.to_csv(STUDENT_COURSE, index=False)

        rprint(f"[green]✅ Successfully removed student with ID {student_id}.[/green]")
        return True

    def delete_all_students(self):
        confirmation = input("⚠️  This will permanently delete student data files from disk. Type 'DELETE' to confirm: ")
        if confirmation.strip().upper() == "DELETE":
            deleted_files = []
            for file_path in [USER_CSV_FILE, STUDENT_COURSE,USER_DATA_FILE]:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
                else:
                    rprint(f"[yellow]⚠️  File not found: {file_path}[/yellow]")

            if deleted_files:
                rprint(f"[bold green]✅ Deleted the following files:[/bold green] {', '.join(deleted_files)}")
            else:
                rprint("[bold red]❌ No files were deleted.[/bold red]")
        else:
            rprint("[yellow]🛑 File deletion cancelled.[/yellow]")

    def export_student_report(self, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_df = self.categorize_by_grade()
        filename = f"student_grade_report_{timestamp}.csv"

        file_path = os.path.join(output_dir, filename)
        report_df.to_csv(file_path, index=False)
        
        rprint(f"[green]✅ Report exported successfully to:[/green] {file_path}")


    def backup_all_student_files(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        files_to_backup = [USER_CSV_FILE, STUDENT_COURSE, USER_DATA_FILE]
        backed_up = []

        for file_path in files_to_backup:
            if os.path.exists(file_path):
                base, ext = os.path.splitext(file_path)
                backup_path = f"{base}_backup_{timestamp}{ext}"
                shutil.copy(file_path, backup_path)
                backed_up.append(backup_path)
            else:
                rprint(f"[yellow]⚠️ File not found (skipped): {file_path}[/yellow]")

        if backed_up:
            rprint(f"[bold green]✅ Backup complete:[/bold green] {', '.join(backed_up)}")
        else:
            rprint("[red]❌ No files were backed up.[/red]")

    @staticmethod
    def get_latest_backup(file_path):
        directory = os.path.dirname(file_path)
        base = os.path.basename(file_path).replace(".csv", "")
        backups = [f for f in os.listdir(directory)
                if f.startswith(base + "_backup") and f.endswith(".csv")]
        backups.sort(reverse=True)
        return os.path.join(directory, backups[0]) if backups else False
    
    def restore_all_student_files(self):

        files_to_restore = [USER_CSV_FILE, STUDENT_COURSE, USER_DATA_FILE]
        restored = []

        for original_file in files_to_restore:
            latest_backup = self.get_latest_backup(original_file)
            if latest_backup and os.path.exists(latest_backup):
                shutil.copy(latest_backup, original_file)
                restored.append(original_file)
            else:
                rprint(f"[yellow]⚠️ No backup found for: {original_file}[/yellow]")

        if restored:
            rprint(f"[bold green]✅ Restored files:[/bold green] {', '.join(restored)}")
        else:
            rprint("[red]❌ No files were restored.[/red]")
            