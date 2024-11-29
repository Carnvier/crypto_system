import socket, pickle
import account as acc, asset as ast, portfolio as p, cryptohive_db as db

condition = True

def load_account_from_db(username, password):
    account = db.CryptoHiveDB().read_account(username, password)
    return account

def authentication():
    message = client.recv(BUFSIZE)
    print(message.decode('utf-8'))
    if message.decode('utf-8') == 'signup':
        message = client.recv(BUFSIZE)
        user_name, password, balance = message.decode('utf-8').split(',')
        user = acc.Account(user_name.lower().strip(), password.lower().strip(), balance.lower().strip())
        user.create_account()
        response = f'success'
        client.send(response.encode('utf-8'))

    elif message.decode('utf-8') == 'login':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        user_name, password = message.split(',')
        print(message)
        account = load_account_from_db(user_name.strip(), password.strip())
        print(account)
        if account:
            balance = account[0][3]
            response = f'success'
            client.send(response.encode('utf-8'))
            response = f'{balance}'
            client.send(response.encode('utf-8'))
        
        if not account:
            response = 'Fail'
            client.send(response.encode('utf-8'))

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

def run(condition):
    message = client.recv(BUFSIZE)
    message =message.decode('utf-8')
    if message == '1':
        current_assets =  ast.assets
        client.sendall(pickle.dumps(current_assets))
        condition = True
        return condition


    if message == '2':
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        user_name, password, action, amount = message.split(',')
        balance = update_account_balance(user_name.lower().strip(), password.lower().strip(), action.lower().strip(), float(amount.strip()))
        print(balance)
        client.sendall(pickle.dumps(balance))
        condition = True
        return condition


    if message == '3':
        current_assets =  ast.assets
        client.sendall(pickle.dumps(current_assets))
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        print(message)
        user_name, password, asset, quantity, action = message.split(',')
        process_trade(user_name.lower().strip(), password.lower().strip(), asset.title().strip(), int(quantity), action.strip())
        condition = True
        return condition

        
    if message == '4':
        message = client.recv(BUFSIZE)
        message = message.decode('utf-8')
        user_name, password = message.split(',')
        data = db.CryptoHiveDB().read_portfolio(user_name.strip())
        client.sendall(pickle.dumps(data))
        condition = True
        return condition

    if message == '5':
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

# Authentication
authentication()
# Main loop to handle client requests
while condition:
    condition = run(condition)







print(load_account_from_db('ghost', 'ghost12345'))
print(db.CryptoHiveDB().read_portfolio('ghost'))