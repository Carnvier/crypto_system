import socket, pickle
import account as acc, asset as ast, portfolio as p, cryptohive_db as db

condition = True

def load_account_from_db(username, password):
    '''Get user account information from database'''
    account = db.CryptoHiveDB().read_account(username, password)
    return account
    

def update_account_balance(username, password, action, amount):
    account = acc.Account(username, password)
    total = account.update_balance(action, amount)
    return total

def process_trade(username, password, asset, quantity, action):
    process =  p.Portfolio()
    if action.lower().startswith('b'):
        process.buy_asset(username, password, asset, quantity)
    elif action.lower().startswith('s'):
        process.sell_asset(username, password, asset, quantity)
    process.save_transaction(username, asset, quantity, action)



def run(message, condition):
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
            client.send(response.encode('utf-8'))
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


    elif message == '1':
        try:
            current_assets =  ast.Asset().get_values()
            print(current_assets)
            client.sendall(pickle.dumps(current_assets))
        except Exception as e:
            print(f'Error: {e}')
        condition = True
        return condition

    elif message == "view_account":
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        user_name, password = message.split(',')
        account = load_account_from_db(user_name.lower().strip(), password.lower().strip())
        client.sendall(pickle.dumps(account))
        condition = True
        return condition

    elif message == '2':
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        try:
            user_name, password, action, amount = message.split(',')
            balance = update_account_balance(user_name.lower().strip(), password.lower().strip(), action.lower().strip(), float(amount.strip()))
            print(balance)
            client.sendall(pickle.dumps(balance))
        except Exception as e:
            print(f'Error: {e}')
        condition = True
        return condition


    elif message == '3':
        try:
            message = client.recv(BUFSIZE)
            message = (message.decode('utf-8'))
            print(message)
            user_name, password, asset, quantity, action = message.split(',')
            process_trade(user_name.lower().strip(), password.lower().strip(), asset.title().strip(), int(quantity), action.strip())
        except Exception as e:
            print(f'Error: {e}')
        condition = True
        return condition

    #  get current holdings for specified user
    elif message == '4':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        print(f"Here is: \n{message}")
        user_name, password = message.split(',')
        data = db.CryptoHiveDB().read_portfolio(user_name.strip())
        client.sendall(pickle.dumps(data))
        condition = True
        return condition
    
    
    # close holdings 
    elif message == '5':
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


    # logout of account and shutdown client and server
    elif message == '6':
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







print(load_account_from_db('ghost', 'ghost12345'))
print(db.CryptoHiveDB().read_portfolio('ghost'))