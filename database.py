import random
import json
from AbstractClass import Agent, Customer

random.seed(1234)
minRand = 10000
maxRand = minRand * 10
numbers1 = list(range(minRand, maxRand))
numbers2 = list(range(0, maxRand))
random.shuffle(numbers1)
random.shuffle(numbers2)
totNum1, totNum2, totAccCreated = 0, 0, 0
# To prevent using an already used random account number, I do this:
# Generate 2 random numbers of 5 digits each, and append them to get the account number
# Just fix the arrays for the 2 rands at the start and pick the next available pair
# This leads to a total of (100000-10000) * 100000 possible accounts = 9,000,000,000(all possible 10-digit nums)

def getNextAccountNumber():
    global totNum1, totNum2, totAccCreated

    rand = numbers1[totNum1] * 100000 + numbers2[totNum2]
    totNum2 += 1
    if totNum2 == len(numbers2):
        totNum1 += 1
        totNum2 = 0
        random.shuffle(numbers2)
    totAccCreated += 1
    return str(rand)

# Custom Encoder is necessary for database to write to json file in the correct format
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Customer) or isinstance(obj, Agent):
            return obj.to_dict()
        return super().default(obj)

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def _update_total_accounts(self, loaded_data):
        global totNum1, totNum2, totAccCreated
        user_list = loaded_data.get("customer", [])
        while totAccCreated<len(user_list):
            getNextAccountNumber()
            
    def _read_data(self):
        try:
            with open(self.db_file, "r") as file:
                loaded_data = json.load(file)
            self._update_total_accounts(loaded_data)
            return loaded_data
        except FileNotFoundError:
            return {"customer": [], "agent": []}
        
    def _write_data(self, data_to_write):
        with open(self.db_file, "w") as file:
            json.dump(data_to_write, file, indent=4, cls=CustomEncoder)

    def _find_user_by_email(self, email, user_list):
        for user in user_list:
            if user["email"] == email:
                return user
        return None
    
    def _find_user_by_account_number(self, account_number, user_list):
        for user in user_list:
            if user["account_number"] == account_number:
                return user
        return None

    def add_user(self, user, user_type):
        existing_data = self._read_data()
        existing_data[user_type].append(user)
        self._write_data(existing_data)
    
    def get_user_email(self, email, user_type):
        data = self._read_data()
        user_list = data.get(user_type, [])
        return self._find_user_by_email(email, user_list)
    
    def get_user_account_number(self, account_number, user_type):
        data = self._read_data()
        user_list = data.get(user_type, [])
        return self._find_user_by_account_number(account_number, user_list)

    def update_user(self, updated_user, user_type):
        data = self._read_data()
        user_list = data.get(user_type, [])
        for i, user in enumerate(user_list):
            if user["email"] == updated_user["email"]:
                user_list[i] = updated_user
                self._write_data(data)
                return True
        return False

    def delete_user(self, del_user):
        data = self._read_data()
        user_list = data.get(del_user["user_type"], [])
        for i, user in enumerate(user_list):
            if user["account_number"] == del_user["account_number"]:
                del user_list[i]
                self._write_data(data)
                return True
        return False