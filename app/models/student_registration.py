import os 
import csv 

from app.constants import USER_DATA_FILE,USER_CSV_FILE,STUDENT_COURSE
class RegistrationUtils:
    @staticmethod
    def generate_student_id():
        existing_ids = set()
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts:
                    existing_ids.add(int(parts[0]))

        for i in range(1, 1000000):
            if i not in existing_ids:
                return f"{i:06d}"
        raise ValueError("❌ No available student IDs left!")
    
    @staticmethod 
    def convert_data_file_to_csv():
        with open(USER_DATA_FILE, 'r') as infile, open(USER_CSV_FILE, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['StudentID', 'Email', 'Password', 'FirstName','LastName'])  # Header
            for line in infile:
                row = line.strip().split(',')
                writer.writerow(row)


class Registration:
    def __init__(self,file_path=USER_DATA_FILE):
        self.file_path=file_path
        self.all_data_path=USER_CSV_FILE
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                pass
            RegistrationUtils.convert_data_file_to_csv()
            self.file_created = True  
        else:
            self.file_created = False
        
        if not os.path.exists(STUDENT_COURSE):
            os.makedirs(os.path.dirname(STUDENT_COURSE), exist_ok=True)  # Ensure directory exists
            with open(STUDENT_COURSE, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['StudentID','Subjects'])  # Write only headers
     
    
    def registeration_file_status(self):
        if self.file_created:
            return(f"✅ File '{USER_DATA_FILE}' created.")
        else:
            return(f"ℹ️ File '{USER_DATA_FILE}' already exists.")

    def register_student(self,email,password,first_name,last_name):
        self.email=email
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.student_id=RegistrationUtils.generate_student_id()
        try:
            with open(USER_DATA_FILE, 'a') as file:
                file.write(f"{self.student_id},{self.email},{self.password},{self.first_name},{self.last_name}\n")
                file.close()
            RegistrationUtils.convert_data_file_to_csv()    
            return True
        except Exception as e:
            return False



