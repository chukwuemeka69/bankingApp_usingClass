from abc import ABC, abstractmethod

# Base class for both Agents and Customers
class Account(ABC):
    def __init__(self, first_name, last_name, email, password, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_type = user_type
        
    @abstractmethod
    def to_dict(self):
        pass

class Agent(Account):
    def __init__(self, first_name, last_name, email, password, user_type):
        super().__init__(first_name, last_name, email, password, user_type)
        
    # To convert an Agent Class to a dictionary to store in JSON file
    def to_dict(self):
        return {
            "user_type": "agent",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }
        
class Customer(Account):
    def __init__(self, first_name, last_name, email, password, user_type, account_number, account_pin, account_balance=0.00):
        super().__init__(first_name, last_name, email, password, user_type)
        self.account_number = account_number
        self.account_pin = account_pin
        self.account_balance = account_balance
        
    # To convert a Customer Class to a dictionary to store in JSON file
    def to_dict(self):
        return {
            "user_type": "customer",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "account_number": self.account_number,
            "account_pin": self.account_pin,
            "account_balance": self.account_balance
        }