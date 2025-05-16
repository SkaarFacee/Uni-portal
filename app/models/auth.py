import re
import pandas as pd
import os

from app.constants import USER_CSV_FILE, USER_DATA_FILE, STUDENT_ID_COL_NAME

LOGIN_STATS_FILE = "login_stats.csv"  # Save in project root or set proper path

class Validate:
    @staticmethod
    def validate_password(password):
        pattern = r'^[A-Z][a-zA-Z]{4,}\d{3,}$'
        return bool(re.match(pattern, password))

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]{1,64}@university\.com$"
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def check_email_exist(email):
        if not os.path.exists(USER_CSV_FILE):
            return False
        return email in pd.read_csv(USER_CSV_FILE)['Email'].tolist()

    @staticmethod
    def get_user_profile(email):
        if not os.path.exists(USER_CSV_FILE):
            return False
        df = pd.read_csv(USER_CSV_FILE, dtype={STUDENT_ID_COL_NAME: str})
        if email in df['Email'].tolist():
            return df[df['Email'] == email]
        return False


class Authentication:
    def __init__(self):
        self.login_attempts = 0
        self.users_df = None
        self.login_stats_df = self.load_login_stats()

    def load_users_df(self):
        if os.path.exists(USER_CSV_FILE):
            self.users_df = pd.read_csv(USER_CSV_FILE, dtype={STUDENT_ID_COL_NAME: str})
        else:
            self.users_df = pd.DataFrame(columns=['StudentID', 'Email', 'Password', 'FirstName', 'LastName'])

    def validate_credentials(self, email, password):
        self.load_users_df()
        if self.users_df.empty:
            return False

        match = self.users_df[
            (self.users_df['Email'] == email) & 
            (self.users_df['Password'] == password)
        ]

        if not match.empty:
            self.record_login(email)
            return True
        return False

    def reset_password(self, email, new_password):
        self.load_users_df()
        if Validate.check_email_exist(email):
            self.users_df.loc[self.users_df['Email'] == email, 'Password'] = new_password
            self.save_users_df()
            return True
        return False

    def save_users_df(self):
        self.users_df.to_csv(USER_CSV_FILE, index=False)
        with open(USER_DATA_FILE, 'w') as file:
            for _, row in self.users_df.iterrows():
                file.write(f"{row['StudentID']},{row['Email']},{row['Password']},{row['FirstName']},{row['LastName']}\n")

    def check_old_password_equals_new(self, email, new_password):
        self.load_users_df()
        if Validate.check_email_exist(email):
            old_password = self.users_df.loc[self.users_df['Email'] == email, 'Password'].values[0]
            return new_password == old_password
        else:
            print('There is no email')
            return False

    def get_student_id(self, email):
        self.load_users_df()
        if Validate.check_email_exist(email):
            return self.users_df.loc[self.users_df['Email'] == email, 'StudentID'].values[0]
        else:
            print('There is no email')
            return None

    # ✅ TASK 111: Login Statistics Tracking
    def load_login_stats(self):
        if os.path.exists(LOGIN_STATS_FILE):
            return pd.read_csv(LOGIN_STATS_FILE)
        return pd.DataFrame(columns=['Email', 'LoginCount'])

    def record_login(self, email):
        # Check if email already in stats
        if email in self.login_stats_df['Email'].values:
            self.login_stats_df.loc[self.login_stats_df['Email'] == email, 'LoginCount'] += 1
        else:
            new_entry = pd.DataFrame([[email, 1]], columns=['Email', 'LoginCount'])
            self.login_stats_df = pd.concat([self.login_stats_df, new_entry], ignore_index=True)

        # Save stats back to CSV
        self.login_stats_df.to_csv(LOGIN_STATS_FILE, index=False)

    def get_login_statistics(self):
        return self.login_stats_df