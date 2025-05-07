USER_DATA_FILE='app/models/data/students.data'
USER_CSV_FILE='app/models/data/complete_data.csv'
COURSES_FILE='app/models/data/courses.csv'
STUDENT_COURSE='app/models/data/student_course_mapping.csv'
STUDENT_ID_COL_NAME='StudentID'
SUBJECT_COL_NAME='Subjects'
SUBJECT_ID_COL='Subject_ID'
MAX_ENROLLMENT_COLS=4
GRADING_SCHEME = [
    (85, 'HD'),  
    (75, 'D'),   
    (65, 'C'),   
    (50, 'P'),   
    (0,  'Z')    
]
class MENU:
    LOGIN="Login"
    REGISTER="Register"
    CANCEL="Cancel"

class ERRORS:
    EMAIL_VALIDATION_ERROR='email_invalid'
    PASSWORD_VALIDATION_ERROR='password_invalid'
    USER_ALREDY_EXISTS_ERROR='user_email_exists'
    ALREADY_LOGGED_IN_ERROR='logged_in_already'

class MGS:
    SUCESS_LOGIN='login_success'
    TOO_MANY_ATTEMPTS='max_attemps_reached'
    TRY_PASSWORD_AGAIN='try_password'
    TRY_EMAIL_AGAIN='try_email'

class LANDING_MSGS:
    PROFILE='profile'
    ENROLLMENTS='enrollments'
    LOG_OUT='log_out'
    ADD_ENROLL='add_enrol'
    VIEW_ENROLL='view_enrol'
    SUBJECT_INFO='subject_info'
    BACK='back'