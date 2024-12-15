import socket, pickle
import time
import portfolio as p
from gui import setup_gui



def login(user_name, password):
    '''Sends password and username to server and returns confirmation message'''
    message = f'login'
    s.send(message.encode('utf-8'))
    message = f'{user_name}, {password}'
    s.send(message.encode('utf-8'))
    balance = s.recv(BUFSIZE)
    try:                                                    
        balance = float(balance.decode('utf-8'))
        print(f'Your current balance: {balance:.2f}')
        return f"{user_name}, {password}, {balance}"
    except:
        return balance.decode('utf-8')

def signup(user_name, password, deposit):
    '''sends signup details to server'''
    message = "signup"
    s.send(message.encode("utf-8"))
    message = f"{user_name}, {password}, {deposit}"
    s.send(message.encode("utf-8"))
    response = s.recv(BUFSIZE)
    response = response.decode("utf-8")

    try:
        user_name, password, balance = response.split(',')
        print("Account successfully created") 
        print(f"Welcome {user_name}! You have a current balance of {balance}.")
        return f"{user_name}, {password}, {balance}"
    except:
        print(response)
        return response
    

def view_account(username, password):
    '''Request user account information'''
    message = "view_account"
    s.send(message.encode("utf-8"))
    message = f"{username}, {password}"
    s.send(message.encode("utf-8"))
    response = s.recv(BUFSIZE)
    response = pickle.loads(response)
    return response


def add_funds(user_name, password, amount):
    """Send deposit details to server and returns the confirmation to gui"""
    message = "deposit_withdraw"
    s.send(message.encode("utf-8"))
    message = f"{user_name}, {password}, deposit, {amount}"
    s.send(message.encode("utf-8"))
    balance = s.recv(BUFSIZE)
    try:
        balance = pickle.loads(balance)
        return(f"Funds successfully deposited Your new balance is: {balance:.2f}")
    except Exception as e:
        balance = balance.decode("utf-8")
        return(f'{balance}') 


def withdraw_funds(user_name, password, amount):
    '''Send withdrawal details to server and returns the confirmation to gui'''
    message = "deposit_withdraw"
    s.send(message.encode("utf-8"))
    message = f"{user_name}, {password}, withdraw, {amount}"
    s.send(message.encode("utf-8"))
    balance = s.recv(BUFSIZE)
    try:
        balance = pickle.loads(balance)
        return(f"Funds successfully withdrawn. Your new balance is: {balance:.2f}")
    except:
        balance = balance.decode("utf-8")
        print (balance)
        return(f'{balance}')


def execute_trade(user_name, password, asset, quantity, action):
    '''Executing a trade on the server and returns the confirmation to gui'''
    message = "execute_trade"
    s.send(message.encode("utf-8"))
    try:
        message = f"{user_name}, {password}, {asset}, {quantity}, {action}"
        message = message.encode("utf-8")
        s.send(message)
        response = s.recv(BUFSIZE)
        response = response.decode("utf-8")
        return response
    except Exception as e:
        return f'Error: {e}'

def view_portfolio(user_name, password):
    '''Viewing current holdings'''
    message = "view_holdings"
    s.send(message.encode("utf-8"))
    message = f'{user_name}, {password}'
    s.send(message.encode("utf-8"))
    length_bytes = s.recv(4)
    if not length_bytes:
        return None
    length = int.from_bytes(length_bytes, byteorder='big')

    data = bytearray()
    while len(data) < length:
        packet = s.recv(min(length - len(data), 4096))  # Receive in chunks of 4096 bytes
        if not packet:
            break
        data.extend(packet)
    try:
        data = pickle.loads(data)
        return data
    except Exception as e:
        return f"Error while loading: {e}"
    
def close_trade(user_name, password, holding_id):
    ''''CLosing specified current holding sending data to server and display response from server'''
    message = "close_trade"
    s.send(message.encode("utf-8"))
    message =  f'{user_name}, {password}, {holding_id}'
    s.send(message.encode("utf-8"))
    # displaying response from server
    response = s.recv(BUFSIZE)
    try:
        response = response.decode("utf-8")
        print(response)
        profit, total, balance = response.split(',')
        return(f"PROFIT: {profit}\nTotal: {total}\nBalance: {balance}")
    except:
        return response
    
def view_transactions(user_name, password):
    '''Requesting server to view user's transaction history'''
    message = "view_transactions"
    s.send(message.encode("utf-8"))
    message = f'{user_name}, {password}'
    s.send(message.encode("utf-8"))
    length_bytes = s.recv(4)
    if not length_bytes:
        return None
    length = int.from_bytes(length_bytes, byteorder='big')

    data = bytearray()
    while len(data) < length:
        packet = s.recv(min(length - len(data), 4096))  # Receive in chunks of 4096 bytes
        if not packet:
            break
        data.extend(packet)
    try:
        data = pickle.loads(data)
        return data
    except Exception as e:
        return f"Error while loading: {e}"
    


def logout():
    '''Requesting server to logout user'''
    confirm = input("Are you sure you want to logout?" )
    if confirm.lower().startswith("y"):
        message = "logout"
        s.send(message.encode("utf-8"))
        response = s.recv(BUFSIZE)
        print("You have been logged out")
        s.close()



# client-server setup
HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDRESS)
print('Connected to server')
# Running main program



client_functions = {
    "login": login,
    "signup": signup,
    "withdraw_funds": withdraw_funds,
    "deposit_funds": add_funds,
    "execute_trade": execute_trade,
    "view_account": view_account,
    "view_holdings": view_portfolio,
    "close_position":close_trade,
    "view_transactions": view_transactions,
    "logout": logout,
}

app = setup_gui(client_functions)
app.mainloop()