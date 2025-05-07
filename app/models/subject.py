from abc import ABC,abstractmethod
from app.constants import GRADING_SCHEME, SUBJECT_ID_COL



class AbstractSubject(ABC):
    @abstractmethod
    def mark_to_grade(mark):
        pass

    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def get_rating():
        pass

    @abstractmethod
    def get_course_info():
        pass


class Subject(AbstractSubject):
    def __init__(self,subject_id,mark):
        super().__init__()
        self.subject_id=subject_id
        self.mark=mark
    @staticmethod
    def mark_to_grade(mark):
        for threshold, grade in GRADING_SCHEME:
            if mark >= threshold:
                return grade
            
    def get_course_info(self,courses_df):
        self.course_info=courses_df[courses_df[SUBJECT_ID_COL]==self.subject_id] 
        if not self.course_info.empty:
            return True
        else:
            return False  

    def get_name(self):
        return self.course_info['Course Name'].values[0]
    
    def get_rating(self):
        return self.course_info['Course Rating'].values[0]
    
    def get_difficulty(self):
        return self.course_info['Difficulty Level'].values[0]
    
    def get_description(self):
        return self.course_info['Course Description'].values[0]
    
    def get_skills(self):
        return self.course_info['Skills'].values[0]
