from AbstractClass import Agent, Customer
from database import Database

db = Database("data.json")
global cur_user

def depositFund():
    print("")
    print("Welcome to Deposit Funds!")
    
    accNum = input("Enter the customer's account number: ")
    user = db.get_user_account_number(accNum, "customer")
    
    if user == None:
        print("There is no account associated with the recipient's account number")
        return
    
    customer = Customer(**user)    # Convert to class
    
    amount = float(input(f"Enter the amount to deposit to {customer.first_name} {customer.last_name}: "))
    
    if amount <= 0:
        print("Invalid amount")
        return
    
    # Transfer and Update Databases
    customer.account_balance += amount
    db.update_user(customer.to_dict(),customer.user_type)

    print(f"Successfully deposited #{amount} to {customer.first_name} {customer.last_name}")
    print("")

def changePin():
    # Requires new pin and customers account Number
    print("")
    print("Welcome to Change Pin!")
    
    accNum = input("Enter the account number to change pin: ")
    user = db.get_user_account_number(accNum, "customer")
    if user == None:
        print("There is no account associated with this account number")
        return
    
    newPin = input("Enter your new pin: ")
    newPin2 = input("Confirm your new pin: ")
    if newPin != newPin2:
        print("Pins do not match")
        return
    
    # Update user pin and database
    user["account_pin"] = newPin
    db.update_user(user, "customer")
    
    print("Successfully changed the Customer Account Pin")
    print("")

def deleteAccount():
    print("")
    print("Welcome to Delete Account!")
    
    accNum = input("Enter the account number to be deleted: ")
    del_user = db.get_user_account_number(accNum, "customer")
    if del_user == None:
        print("There is no account associated with this account number")
        return
    
    response = input("Are you sure you want to delete this account? y/n: ")
    if response != "y":
        return
    
    # Update database
    db.delete_user(del_user)
    
    print("Successfully deleted Customer Account")
    print("")

def resetPassword():
    print("")
    print("Welcome to Reset Password!")
    
    remember = input("Do you know the old password? Type 'y' for yes or any key for no: ")
    print("Input the account details")
    if remember=="y":
        password = input("Enter your old password: ")
        if cur_user.password != password:
            print("The password is not correct")
            return
    else:
        email = input("Input your email: ")
        if email != cur_user.email:
            print("Wrong email")
            return
        
    newPassword = input("Enter your new password: ")
    newPassword2 = input("Confirm your new password: ")
    if newPassword != newPassword2:
        print("Passwords do not match")
        return
    
    # Update database
    cur_user.password = newPassword
    db.update_user(cur_user.to_dict(),cur_user.user_type)
    
    print("You have successfully changed your password")
    print("")

def agent_main(user):
    global cur_user
    cur_user = user
    
    while True:
        print("")
        print(f"Welcome to Bank Management System for Agents!, {cur_user.first_name}")
        print("0. Exit the Program")
        print("1. Fund Customer Account")
        print("2. Change Customer Pin")
        print("3. Delete Customer Account")
        print("4. Reset Account Password")
        
        key = int(input("Type a key to choose your option: "))
        print("")
        
        if key==0:
            print("Thanks for visiting, see you next time!")
            break
        elif key==1:
            depositFund()
        elif key==2:
            changePin()
        elif key==3:
            deleteAccount()
        elif key==4:
            resetPassword()
        else:
            print("That is an invalid option")
            

if __name__ == "__main__":
    # This code block will only execute when agent.py is run directly, not when imported as a module.
    # Set a dummy Agent  that is not stored to the database
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "random password",
        "user_type": "agent"
    }
    agent_main(Agent(**user_data))        # Convert dictionary to class, use as parameter