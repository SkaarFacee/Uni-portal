from abc import ABC, abstractmethod

class LoginController(ABC):
    @abstractmethod 
    def __init__(self,email,password):
        pass
    @abstractmethod          
    def login(self):
        pass
    
    @abstractmethod          
    def get_user(self):
        pass
