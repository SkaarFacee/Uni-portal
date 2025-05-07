import os 
import sys

def change_dir():
        

    files_in_cwd = os.listdir(os.getcwd())

    if 'cli.py' in files_in_cwd:
        project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
    else:
        project_root = os.path.abspath(os.path.join(os.getcwd()))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)  
