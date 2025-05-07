from abc import ABC, abstractmethod

class User(ABC): 
    def __init__(self,email,password):
        self.email=email
        self.password=password
    @abstractmethod          
    def login(self):
        pass