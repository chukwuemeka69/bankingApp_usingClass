from AbstractClass import Customer
from database import Database

db = Database("data.json")
global cur_user

def printAccount():
    global cur_user
    print("")
    print("These are your account details:")
    print(f"First Name: {cur_user.first_name}")
    print(f"Last Name: {cur_user.last_name}")
    print(f"Email: {cur_user.email}")
    print(f"Password: {cur_user.password}")
    print(f"Account Number: {cur_user.account_number}")
    print(f"Account pin: {cur_user.account_pin}")
    print(f"Account balance: {cur_user.account_balance}")
    print("")
    
def transferFund():
    print("")
    print("Welcome to Transfer Funds!")
    
    pin = input("Enter your pin number: ")
    if pin != cur_user.account_pin:
        print("Wrong pin number")
        return
    
    accNum = input("Enter the recipient's account number: ")
    user2 = db.get_user_account_number(accNum, "customer")
    if user2 == None:
        print("There is no account associated with the recipient's account number")
        return
    
    customer2 = Customer(**user2) # Convert to class
    
    amount = float(input(f"Enter the amount to send to {customer2.first_name} {customer2.last_name}: "))
    
    if amount <= 0:
        print("Invalid amount")
        return
    
    if(amount > cur_user.account_balance):
        print("Insufficient Funds")
        return
    
    # Transfer amount
    cur_user.account_balance -= amount
    customer2.account_balance += amount
    
    # Update database
    db.update_user(cur_user.to_dict(),cur_user.user_type)
    db.update_user(customer2.to_dict(),customer2.user_type)

    print(f"Successfully sent #{amount} to {customer2.first_name} {customer2.last_name}")
    print("")


def resetPassword():
    print("")
    print("Welcome to Reset Password!")
    
    remember = input("Do you know the old password? Type 'y' for yes or any key for no: ")
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

def customer_main(user):
    global cur_user
    cur_user = user           # get the logged in user's account from the parameters
    
    while True:
        print("")
        print(f"Welcome to Bank Management System for Customers!, {cur_user.first_name}")
        print("0. Exit the Program")
        print("1. View Account Info")
        print("2. Transfer to an Account")
        print("3. Reset Password")
        
        key = int(input("Type a key to choose your option: "))
        print("")
        
        if key==0:
            print("Thanks for visiting, see you next time!")
            break
        elif key==1:
            printAccount()
        elif key==2:
            transferFund()
        elif key==3:
            resetPassword()
        else:
            print("That is an invalid option")

if __name__ == "__main__":
    # This code block will only execute when customer.py is run directly, not when imported as a module.
    # Set a dummy Customer that is not stored to the database
    user_data = {
        "first_name": "John",
        "last_name": "Ilozor",
        "email": "johnilozor@gmail.com",
        "password": "password1234",
        "account_number": "1234567890",
        "account_pin": "9876",
        "user_type": "customer",
        "account_balance": 150000
    }
    customer_main(Customer(**user_data))      # Convert dictionary to class, use as parameter