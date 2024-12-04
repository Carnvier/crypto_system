import socket, pickle
import time
import portfolio as p

condition = True

def display_account():
    print("*"*10, "Welcome to DGTraders", "*"*10 )
    account = input("Do you have an account? (y/n): ")
    # collecting data for account creation
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

        # printing response from server
        try:
            user_name, password, balance = response.split(',')
            print("Account successfully created") 
            print(f"Welcome {user_name}! You have a current balance of {balance}.")
            return user_name, password
        except:
                print(response)
                # if account creation fails, tells user to try again.
                return display_account()

    elif account.lower().startswith("y"):    
        message = f'login'
        s.send(message.encode('utf-8'))
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        message = f'{user_name}, {password}'
        s.send(message.encode('utf-8'))
        balance = s.recv(BUFSIZE)
        try:
            balance = float(balance.decode('utf-8'))
            print(f'Your current balance: {balance:.2f}')
            return user_name, password
        except:
            print(f'Your password or username is incorrect. Please try again')
            return display_account()
    else:
        print("Invalid option. Please try again.")
        return display_account()

def view_assets():
    assets = s.recv(BUFSIZE)
    try:
        assets = pickle.loads(assets)
        print("Current assets:")
        for asset, value in assets.items():
            print(f"{asset:<10}: {value}")
    except Exception as e: 
        print(f"Error while loading: {e}")


def add_funds(user_name, password, amount):
    message = f"{user_name}, {password}, deposit, {amount}"
    s.send(message.encode("utf-8"))
    try:
        balance = s.recv(BUFSIZE)
        balance = pickle.loads(balance)
        print("Funds successfully deposited")
        print(f"Your new balance is: {balance:.2f}")
    except Exception as e:
        print(f"Error: {e}")


def withdraw_funds(user_name, password, amount):
    message = f"{user_name}, {password}, withdraw, {amount}"
    s.send(message.encode("utf-8"))
    try:
        balance = s.recv(BUFSIZE)
        balance = pickle.loads(balance)
        print("Funds successfully withdrawn")
        print(f"Your new balance is: {balance:.2f}")
    except Exception as e:
        print(f"Error: {e}")


def execute_trade(user_name, password, asset, quantity, action):
    message = f"{user_name}, {password}, {asset}, {quantity}, {action}"
    message = message.encode("utf-8")
    s.send(message)
    

def view_portfolio(user_name, password):
    '''Viewing current holdings'''
    message = f'{user_name}, {password}'
    s.send(message.encode("utf-8"))
    data = s.recv(BUFSIZE)
    try:
        data = pickle.loads(data)
        p.Portfolio().view_holdings(user_name, data)
    except Exception as e:
        print(f"Error while loading: {e}")

def close_trade(user_name, password, holding_id):
    ''''CLosing specified current holding sending data to server and display response from server'''
    message =  f'{user_name}, {password}, {holding_id}'
    s.send(message.encode("utf-8"))
    # displaying response from server
    response = s.recv(BUFSIZE)
    try:
        response = response.decode("utf-8")
        print(response)
        profit, total, balance = response.split(',')
        print(f"PROFIT: {profit}\nTotal: {total}\nBalance: {balance}")
    except Exception as e:
        print(f"Error: {e}")
    condition = True
    return condition


def logout(condition):
    confirm = input("Are you sure you want to logout?" )
    if confirm.lower().startswith("y"):
        message = "6"
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
        print("1. View Asset \n2. Deposit and Withdraw \n3. Trade \n4. View Holdings \n5. Close Holding \n6. Logout")
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

        # display current holdings
        if option == '4':
            message = "4"
            s.send(message.encode("utf-8"))
            view_portfolio(user_name, password)
            continue

        # close a specified holding
        if option == '5':
            message = "5"
            s.send(message.encode("utf-8"))
            view_portfolio(user_name, password)
            # check if input is int
            while True:
                if (holding_id := input("Select holding to close by ID: ")).isdigit():
                    holding_id = int(holding_id)  # Convert to integer if needed
                    break  # Exit the loop if input is valid
                else:
                    print("Please enter an integer value of ID (e.g., 2)!")
            confirmation = input(f"Are you sure you want to close {holding_id} (y/n): ")
            if confirmation.lower().startswith('y'):
                close_trade(user_name, password, holding_id)
            elif confirmation.lower().startswith('n'):
                print("Order cancelled")
            else:
                print("Invalid input. Order cancelled")
            

        if option == '6':
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


