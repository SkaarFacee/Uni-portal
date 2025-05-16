import re 
import pandas as pd 

from app.constants import USER_CSV_FILE,USER_DATA_FILE,STUDENT_ID_COL_NAME,ADM_CSV_FILE,ADM_ID_COL_NAME

class Validate:
    @staticmethod
    def validate_password(password):
        pattern = r'^[A-Z][a-zA-Z]{4,}\d{3,}$'
        return bool(re.match(pattern, password))

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]{1,64}@university\.com$"        
        if re.fullmatch(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def check_email_exist(email,usertype=2):
        if usertype == 1:
            if email in pd.read_csv(ADM_CSV_FILE)['Email'].to_list():
                return True
            else: 
                return False
        elif usertype == 2:
            if email in pd.read_csv(USER_CSV_FILE)['Email'].to_list():
                return True
            else: 
                return 
            


        
    @staticmethod    
    def get_user_profile(email):
        df=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
        if email in df['Email'].to_list():
            return df[df['Email']==email]
        else :
            return False 

class Authentication():
    def __init__(self,user_type=2):
        self.login_attempts=0
        self.user_type = user_type
        
    def load_users_df(self):
        if self.user_type == 1:
            #print('File reading for admin')
            self.users_df=pd.read_csv(ADM_CSV_FILE,dtype={ADM_ID_COL_NAME: str})
        elif self.user_type == 2:
            #print('File reading for student')
            self.users_df=pd.read_csv(USER_CSV_FILE,dtype={STUDENT_ID_COL_NAME: str})
        
    def validate_credentials(self, email, password):
        self.load_users_df()
        if self.users_df.empty:
            return False

        match = self.users_df[
            (self.users_df['Email'] == email) & 
            (self.users_df['Password'] == password)
        ]

        return not match.empty

    def reset_password(self, email, new_password):
        self.load_users_df()
        self.users_df.loc[self.users_df['Email'] == email, 'Password'] = new_password
        self.save_users_df()
        return True

    def save_users_df(self):
        self.users_df.to_csv(USER_CSV_FILE, index=False)
        with open(USER_DATA_FILE, 'w') as file:
            for _, row in self.users_df.iterrows():
                file.write(f"{row['StudentID']},{row['Email']},{row['Password']},{row['FirstName']},{row['LastName']}\n")

    def check_old_password_equals_new(self,email,new_password):
        self.load_users_df()
        if Validate.check_email_exist(email):
            old_password=self.users_df[self.users_df['Email']==email]['Password']
            if new_password == old_password: 
                return True
            else :
                return False
        else:
            print('There is no email')

    def get_student_id(self,email,usertype):
        self.load_users_df()
        if Validate.check_email_exist(email,usertype):
            return self.users_df[self.users_df['Email']==email]['StudentID'].unique()[0]
        else:
            print('There is no email')

    def get_admin_id(self,email,usertype):
        self.load_users_df()
        if Validate.check_email_exist(email,usertype):
            return self.users_df[self.users_df['Email']==email]['AdminID'].unique()[0]
        else:
            print('There is no email')