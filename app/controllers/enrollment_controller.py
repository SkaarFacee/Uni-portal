from rich import print as rprint

from app.models.enrollment import Enrollment
from app.models.subject import Subject

from app.views.cli_landing_view import LandingView

from app.constants import LANDING_MSGS

class EnrollmentController:
    def __init__(self,student_user):
        self.enrollment=Enrollment(student_user)

    
    def menu_choice(self):
        return LandingView.ask_student_view()

            
    def enroll_menu(self):
        LandingView.enrollment_landing()
        if self.enrollment.check_enrollment_completion():
            LandingView.enrollment_reached()
        else:
            LandingView.enrollment_pending()
        while True:
            choice=LandingView.ask_enrollment_action()
            match choice:
                case LANDING_MSGS.ADD_ENROLL:
                    # ask if you want random enroll or add by subject id 
                        if not LandingView.ask_random_enroll():
                            if self.enrollment.get_number_of_enrollments()<4:
                                while LandingView.confirm():        
                                    random_df=self.enrollment.get_random_subjects()
                                    subject_choice=LandingView.get_subject_from_df(random_df)
                                    print(f'This is the choice {subject_choice}')
                                    self.enrollment.enroll_subject(subject_choice)
                                    
                            else:
                                rprint('[red]You have already enrolled in 4 subjects')
                        else: 
                            if self.enrollment.add_random_enroll():
                                LandingView.show_enrollments(self.enrollment.get_number_of_enrollments())
                            else:
                                rprint('[red]You have already enrolled in 4 subjects')
                case LANDING_MSGS.VIEW_ENROLL:
                    LandingView.display_student_marks(self.enrollment.view_enrollments())

                    if not self.enrollment.get_number_of_enrollments()>0:
                        rprint("[bold red]⚠️ WARNING: You have no subject enrollments![/bold red]")

                case LANDING_MSGS.SUBJECT_INFO:
                    if self.enrollment.get_number_of_enrollments()>0:
                        subjects_picked=LandingView.ask_subject_selection(self.enrollment.view_enrollments())
                        if LandingView.ask_remove_subject():
                            temp=[self.enrollment.unenroll_subject(sub) for sub in subjects_picked]
                            LandingView.remove_success()
                            
                                
                        else:
                            subjects=[Subject(sub,self.enrollment.view_enrollments()[sub][0]) for sub in subjects_picked]
                            subjects_get_info_response=[s.get_course_info(self.enrollment.courses_df) for s in subjects]
                            if all(subjects_get_info_response):
                                LandingView.display_subject_details(subjects)
                    else:
                        rprint('[red]You have not enrolled in anything')
                case LANDING_MSGS.BACK:
                    break


    def profile_menu(self):
        LandingView.display_profile(self.enrollment.get_student_profile())
        
