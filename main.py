from Customer import Customer, customer_main
from Agent import Agent, agent_main
from database import Database,getNextAccountNumber

db = Database("data.json")

def isEmailUsed(email):
    #check if email is unique
    user1 = db.get_user_email(email,"customer")
    user2 = db.get_user_email(email,"agent")
    return user1 != None or user2 != None

def create_customer():
    print("")
    print("Welcome to Creating a New Customer Account!")
    
    fName=input("Enter your First Name: ")
    lName=input("Enter your Last Name: ")
    email=input("Enter your Email: ")
    password=input("Enter your password: ")
    
    if isEmailUsed(email):
        print("Email has already been used!")
        return
    
    pin = input("Enter your pin number: ")
    
    print("")
    print(f"Hello {fName} {lName}!")
    print("You have successfully made a Customer account")
    
    # Make a new Customer, update to database
    customer = Customer(fName,lName,email,password,"customer",getNextAccountNumber(),pin)
    db.add_user(customer, customer.user_type)
    
    print(f"Your account number is {customer.account_number}")

def create_agent():
    print("")
    print("Welcome to Creating a New Agent Account!")
    
    fName=input("Enter your First Name: ")
    lName=input("Enter your Last Name: ")
    email=input("Enter your Email: ")
    password=input("Enter your password: ")
    
    if isEmailUsed(email):
        print("Email has already been used!")
        return
    
    print("")
    print(f"Hello {fName} {lName}!")
    print("You have successfully made an Agent account")
    
    # Make a new Agent, update to database
    agent = Agent(fName,lName,email,password,"agent")
    db.add_user(agent, agent.user_type)

def login():
    print("")
    print("Welcome to the Login Page!")
    email=input("Enter your Email: ")

    if not isEmailUsed(email):
        print("There is no email associated with this account")
    else:
        password=input("Enter your password: ")
        user = db.get_user_email(email,"customer")    # User email might already be used by a customer account
        
        if user==None:
            user = db.get_user_email(email,"agent")   # User email is used by an agent account instead
            
        if user["password"] != password:
            print("The password is wrong")
        else:
            if user["user_type"]=="customer":
                print("")
                customer_main(Customer(**user))
            else:
                print("")
                agent_main(Agent(**user))
    
def main():
    # This is the main loop with menu options
    while True:
        print("")
        print("Welcome to this Bank Management App!")
        print("0. Exit")
        print("1. Create a Customer Account")
        print("2. Create an Agent Account")
        print("3. Login to your Account")
        
        choice = int(input("Please choose an option: "))
        print("")
        
        if choice == 0:
            print("See you next time!")
            break
        elif choice == 1:
            create_customer()
        elif choice == 2:
            create_agent()
        elif choice == 3:
            login()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
