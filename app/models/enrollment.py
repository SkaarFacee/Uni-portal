import pandas as pd 
import random

from app.constants import COURSES_FILE,STUDENT_COURSE,STUDENT_ID_COL_NAME,STUDENT_ID_COL_NAME,SUBJECT_COL_NAME,MAX_ENROLLMENT_COLS,SUBJECT_ID_COL
from app.models.user_student import Student
from app.models.subject import Subject
from app.models.auth import Validate
import ast 
class EnrollmentUtils:
    @staticmethod
    def prepare_courses_df():
        df=pd.read_csv(COURSES_FILE)
        df.drop(['University',"Course URL"],axis=1,inplace=True)
        return df
    
    @staticmethod
    def prepare_student_course_df():
        return pd.read_csv(STUDENT_COURSE,dtype={STUDENT_ID_COL_NAME: str},index_col=None)
    
    @staticmethod
    def update_student_course_df(df):
        return df.to_csv(STUDENT_COURSE,index=False)

    @staticmethod 
    def check_if_id_in_enrolled_subjects(idx,enrolled):
        return True if idx in enrolled else False 
   
    @staticmethod
    def check_if_subject_id_valid(subject_id,df):
        return True if subject_id in df[SUBJECT_ID_COL].values else False
    
    @staticmethod
    def get_random_mark():
        return random.randint(1,100)
    
    @staticmethod
    def map_sub_to_mark(subjects):
        return {
                sub: [
                    (mark := EnrollmentUtils.get_random_mark()),
                    Subject.mark_to_grade(mark)
                ]
                for sub in subjects
            }



class Enrollment:
    def __init__(self, student_obj : Student):
        self.student = student_obj
        self.courses_df = EnrollmentUtils.prepare_courses_df()
        self.student_course_df = EnrollmentUtils.prepare_student_course_df()
        
        # Fix for missing student_id attribute
        if not hasattr(self.student, 'student_id') or self.student.student_id is None:
            try:
                # Get student_id directly from CSV
                import pandas as pd
                from app.constants import USER_CSV_FILE, STUDENT_ID_COL_NAME
                
                # Read the user data
                users_df = pd.read_csv(USER_CSV_FILE, dtype={STUDENT_ID_COL_NAME: str})
                user_row = users_df[users_df['Email'] == self.student.email]
                
                if not user_row.empty:
                    self.student.student_id = user_row[STUDENT_ID_COL_NAME].values[0]
                    # print(f"Retrieved student_id: {self.student.student_id} for email: {self.student.email}")
                    
                    # Initialize enrolled_subjects if it doesn't exist
                    if not hasattr(self.student, 'enrolled_subjects'):
                        self.student.enrolled_subjects = {}
                else:
                    raise AttributeError(f"Could not find student with email {self.student.email} in the database")
            except Exception as e:
                print(f"Error retrieving student_id: {e}")
                raise
        
        self.add_student_if_not_enrolled()

    def check_enrollment_completion(self):
        return True if len(self.student.enrolled_subjects)==4 else False

    def add_student_if_not_enrolled(self):
        try:
            # Make sure student_id is a string for comparison
            student_id_str = str(self.student.student_id)
            
            if self.student_course_df.empty or student_id_str not in self.student_course_df[STUDENT_ID_COL_NAME].astype(str).values:
                self.student.enrolled_subjects = {}
                new_row = {
                    STUDENT_ID_COL_NAME: student_id_str,
                    'Subjects': self.student.enrolled_subjects
                }

                self.student_course_df = pd.concat(
                    [self.student_course_df, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                EnrollmentUtils.update_student_course_df(self.student_course_df)

            elif student_id_str in self.student_course_df[STUDENT_ID_COL_NAME].astype(str).values: 
                row = self.student_course_df[self.student_course_df[STUDENT_ID_COL_NAME].astype(str) == student_id_str]
                if not row.empty:
                    subject_str = row[SUBJECT_COL_NAME].iloc[0]
                    if pd.isna(subject_str) or subject_str == '{}':
                        self.student.enrolled_subjects = {}
                    else:
                        try:
                            self.student.enrolled_subjects = ast.literal_eval(subject_str)
                        except (ValueError, SyntaxError):
                            self.student.enrolled_subjects = {}
            return None
        except Exception as e:
            print(f"Error in add_student_if_not_enrolled: {e}")
            self.student.enrolled_subjects = {}
        return None
    
    def update_student_course(self):
        if self.student.student_id in self.student_course_df[STUDENT_ID_COL_NAME].values:
            self.student_course_df.loc[
                self.student_course_df[STUDENT_ID_COL_NAME] == self.student.student_id,
                'Subjects'
            ] = [self.student.enrolled_subjects]
            EnrollmentUtils.update_student_course_df(self.student_course_df)
        return True

    def get_number_of_enrollments(self):
        return len(self.student.enrolled_subjects)

    def view_enrollments(self):
        return self.student.enrolled_subjects
    
    def add_random_enroll(self):
        if not self.check_enrollment_completion():
            subjects=self.courses_df.sample(MAX_ENROLLMENT_COLS-self.get_number_of_enrollments())[SUBJECT_ID_COL].to_list()
            self.student.enrolled_subjects.update(EnrollmentUtils.map_sub_to_mark(subjects))
            if self.update_student_course():
                return True
        else: 
            return False

    def unenroll_subject(self,subject_id):
        if self.get_number_of_enrollments()==0:
            print('Nothing to unenroll')
            return None
        if EnrollmentUtils.check_if_id_in_enrolled_subjects(subject_id,self.student.enrolled_subjects):
            del self.student.enrolled_subjects[subject_id]
            self.update_student_course()
            return True 
        return False 
    
    def enroll_subject(self,subject_id):
        if self.get_number_of_enrollments()>=5:
            return None
        
        if isinstance(subject_id, str) and EnrollmentUtils.check_if_subject_id_valid(subject_id, self.courses_df):
            mark = EnrollmentUtils.get_random_mark()
            grade = Subject.mark_to_grade(mark)
            self.student.enrolled_subjects[subject_id] = [mark, grade]
            
            self.update_student_course()
            return True
        else:
            return False
        
    
    def get_student_profile(self):
        return Validate.get_user_profile(self.student.email)
    
    def get_random_subjects(self):
        return self.courses_df.sample(5)
