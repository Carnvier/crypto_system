import socket, pickle
import account as acc, asset as ast, portfolio as p, cryptohive_db as db

condition = True

def load_account_from_db(username, password):
    '''Get user account information from database'''
    account = db.CryptoHiveDB().read_account(username, password)
    return account
    

def update_account_balance(username, password, action, amount):
    '''function to pass arguments to update balance'''
    account = acc.Account(username, password)
    total = account.update_balance(action, amount)
    return total


def process_trade(username, password, asset, quantity, action):
    '''funtion to pass arguments to process trade'''
    process =  p.Portfolio()
    if action.lower().startswith('b'):
        response = process.buy_asset(username, password, asset, quantity)
    elif action.lower().startswith('s'):
        response = process.sell_asset(username, password, asset, quantity)
    process.save_transaction(username, asset, quantity, action)
    return response


def run(message, condition):
    '''running function that communicates with client'''
    # authentication for login
    if message == 'login':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        user_name, password = message.split(',')
        account = load_account_from_db(user_name.strip(), password.strip())
        # send account balance to server
        try:
            balance = account[0][3]
            response = f'{balance}'
            client.send(response.encode('utf-8'))
        # if no account balance send an error message
        except:
            message = 'Invalid username or password'
            client.send(message.encode('utf-8'))
        condition = True
        return condition


    # creating new account
    elif message == 'signup':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        user_name, password, balance = message.split(',')
        user = acc.Account(user_name.lower().strip(), password.lower().strip(), balance.lower().strip())
        response = user.create_account()
        client.send(response.encode('utf-8'))
        condition = True
        return condition


    # view user account
    elif message == "view_account":
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        user_name, password = message.split(',')
        account = load_account_from_db(user_name.lower().strip(), password.lower().strip())
        client.sendall(pickle.dumps(account))
        condition = True
        return condition

    # deposit or withdraw funds from account
    elif message == 'deposit_withdraw':
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        user_name, password, action, amount = message.split(',')
        balance = update_account_balance(user_name.lower().strip(), password.lower().strip(), action.lower().strip(), float(amount.strip()))
        print(balance)
        if type(balance) == int or type(balance) == float:
            serialized_data = pickle.dumps(balance)
            client.sendall(serialized_data)
        else:
            client.send(balance.encode('utf-8'))
        condition = True
        return condition

    # executing trade for user 
    elif message == 'execute_trade':
        try:
            message = client.recv(BUFSIZE)
            message = (message.decode('utf-8'))
            print(message)
            user_name, password, asset, quantity, action = message.split(',')
            message = process_trade(user_name.lower().strip(), password.lower().strip(), asset.title().strip(), int(quantity), action.strip())
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f'Error: {e}')
        condition = True
        return condition

    #  get current holdings for specified user
    elif message == 'view_holdings':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        print(f"Here is: \n{message}")
        user_name, password = message.split(',')
        data = db.CryptoHiveDB().read_portfolio(user_name.strip())
        print(data)
        serialized_data = pickle.dumps(data)
        client.sendall(len(serialized_data).to_bytes(4, byteorder='big'))
        client.sendall(serialized_data)
        condition = True
        return condition
    
    
    # close holdings 
    elif message == 'close_trade':
        # closing selected holding 
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        print(message)
        user_name, password, holding_id = message.split(',')
        user_name, password, holding_id = user_name.strip(), password.strip(), int(holding_id)
        response = p.Portfolio().close_position(user_name, password, holding_id)
        print(response)
        client.send(response.encode('utf-8'))
        condition = True
        return condition
    
    elif message == 'view_transactions':
        # view all transactions for specified user
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        print(f"Here are: \n{message}")
        user_name, password = message.split(',')
        data = db.CryptoHiveDB().read_transactions(user_name.strip())
        print(data)
        serialized_data = pickle.dumps(data)
        client.sendall(len(serialized_data).to_bytes(4, byteorder='big'))
        client.sendall(serialized_data)
        condition = True
        return condition


    # logout of account and shutdown client and server
    elif message == 'logout':
        print(message)
        print(f"Logging out {client}.")
        message = f'Logging out!'
        client.send(message.encode('utf-8'))
        client.close()
        condition = False
        return condition
        

# client-server setup
HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 4024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)
s.listen(1)
client, address = s.accept()


# Main loop to handle client requests
while condition:
    message = client.recv(BUFSIZE)
    message = message.decode('utf-8')
    condition = run(message, condition)





