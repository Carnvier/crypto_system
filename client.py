import socket, pickle
import time
import portfolio as p

condition = True

def display_account():
    print("*"*10, "Welcome to DGTraders", "*"*10 )
    account = input("Do you have an account? (y/n): ")
    if account.lower().startswith("n"):
        print("Lets get you started...")
        message = "signup"
        s.send(message.encode("utf-8"))
        user_name = input("Please enter your username: ")
        while True:
            password = input("Please enter your password: ")
            confirm_password = input("Please re-enter your password: ")
            if confirm_password == password:
                break
            if confirm_password != password:
                print("Passwords do not match!")
                continue
        deposit = input("Please enter your deposit: ")

        message = f"{user_name}, {password}, {deposit}"
        s.send(message.encode("utf-8"))
        response = s.recv(BUFSIZE)
        if response.decode() == "success":
            print("Account successfully created") 
            return user_name, password
        else:
            print("Error creating account. Please contact administrator")

    elif account.lower().startswith("y"):    
        message = f'login'
        s.send(message.encode('utf-8'))
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        message = f'{user_name}, {password}'
        s.send(message.encode('utf-8'))
        response = s.recv(BUFSIZE)
        if response.decode('utf-8').lower() == 'success':
            balance = s.recv(BUFSIZE)
            balance = float(balance.decode('utf-8'))
            print(f'Your current balance: {balance:.2f}')
            return user_name, password
        elif response.decode('utf-8').lower() == 'fail':
            print(f'Your password for {user_name} is incorrect. Please try again')
            return

def view_assets():
    assets = s.recv(BUFSIZE)
    assets = pickle.loads(assets)
    print("Current assets:")
    for asset, value in assets.items():
        print(f"{asset:<10}: {value}")

def add_funds(user_name, password, amount):
    message = f"{user_name}, {password}, deposit, {amount}"
    s.send(message.encode("utf-8"))
    print("Funds successfully deposited")
    balance = s.recv(BUFSIZE)
    balance = pickle.loads(balance)
    print(f"Your new balance is: {balance:.2f}")

def withdraw_funds(user_name, password, amount):
    message = f"{user_name}, {password}, withdraw, {amount}"
    s.send(message.encode("utf-8"))
    print("Funds successfully withdrawn")
    balance = s.recv(BUFSIZE)
    balance = pickle.loads(balance)
    print(f"Your new balance is: {balance:.2f}")


def execute_trade(user_name, password, asset, quantity, action):
    message = f"{user_name}, {password}, {asset}, {quantity}, {action}"
    message = message.encode("utf-8")
    s.send(message)
    

def view_portfolio(user_name, password):
    message = f"4"
    message = message.encode("utf-8")
    s.send(message)
    message = f'{user_name}, {password}'
    data = s.recv(BUFSIZE)
    data = pickle.loads(data)
    p.Portfolio().view_holdings(user_name, data)


def logout(condition):
    confirm = input("Are you sure you want to logout?" )
    if confirm.lower().startswith("y"):
        message = "5"
        s.send(message.encode("utf-8"))
        response = s.recv(BUFSIZE)
        print("You have been logged out")
        s.close()
        condition = False
    else: 
        condition = True
        return condition
        

def run(condition):
    user_name, password = display_account()
    while condition:
        print("Welcome to the Menu")
        print("1. View Asset \n2. Deposit and Withdraw \n3. Trade \n4. View Holdings \n5. Logout")
        option = input("Select the option from the list above using the number. ")
        
        if option == '1':
            message = "1"
            s.send(message.encode('utf-8'))
            view_assets()
            continue

        if option == '2':
            message = "2"
            s.send(message.encode("utf-8"))
            while True:
                action = str(input("Deposit or Withdraw: "))
                amount = float(input("Enter amount: "))
                if action.lower().startswith('d'):
                    add_funds(user_name, password, amount)
                    break
                elif action.lower().startswith('w'):
                    withdraw_funds(user_name, password, amount)
                    break
                else:
                    print("Invalid action!")
                    continue
            continue

        if option == '3':
            message = "3"
            s.send(message.encode("utf-8"))
            view_assets()
            asset = input("Enter the asset you want to trade: ")
            quantity = input("Enter the quantity: ")
            action = input("Buy or Sell: ")
            execute_trade(user_name, password, asset, quantity, action)
            continue

        if option == '4':
            view_portfolio(user_name)
            continue

        if option == '5':
            condition = logout(condition)  


# client-server setup
HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDRESS)
print('Connected to server')
# Running main program
run(condition)


