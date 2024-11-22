import socket, pickle
import account as acc, asset as ast, portfolio as p

def load_accounts():
    with open('accounts.txt', 'r') as f:
        data = f.readlines()
    return data

def load_portfolios():
    with open('portfolio.txt', 'r') as f:
        data = f.readlines()
    return data

def update_account_balance(username, password, amount, action):
    account = acc.Account(username, password)
    return account.update_balance(action, amount)

def process_trade(username, asset, quantity, action):
    process =  p.Portfolio()
    if action.lower().startswith('b'):
        process.buy_asset(username, asset, quantity)
    elif action.lower().startswith('s'):
        process.sell_asset(username, asset, quantity)
    process.save_transaction(username, asset, quantity, action)

HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 4024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

s.listen(1)



client, address = s.accept()
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
    user_name, password = message.decode('utf-8').split(',')
    accounts = load_accounts()
    login = False
    for line in accounts:
        username, passkey, balance,  = line.split(',')
        if username.lower().strip() == user_name.lower().strip() and passkey.lower().strip() == password.lower().strip():
            response = f'Success'
            client.send(response.encode('utf-8'))
            response = f'{balance}'
            client.send(response.encode('utf-8'))
            login = True
    
    if not login:
        response = 'Fail'
        client.send(response.encode('utf-8'))


def run():
    message = client.recv(BUFSIZE)
    message =message.decode('utf-8')
    if message == '1':
        current_assets =  ast.assets
        client.sendall(pickle.dumps(current_assets))

    if message == '2':
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        user_name, password, action, amount = message.split(',')
        balance = update_account_balance(user_name.lower().strip(), password.lower().strip(), action.strip(), float(amount.strip()))
        client.send(balance.encode('utf-8'))

    if message == '3':
        current_assets =  ast.assets
        client.sendall(pickle.dumps(current_assets))
        message = client.recv(BUFSIZE)
        message = (message.decode('utf-8'))
        asset, quantity, action = message.split(',')
        process_trade(user_name.lower().strip(), asset.strip(), quantity.strip(), action.strip())
        
    if message == '4':
        client.sendall(pickle.dumps(load_portfolios()))

    if message == '5':
        print(message)
        print(f"Logging out {client}.")
        message = f'Logging out!'
        client.send(message.encode('utf-8'))
        client.close()
        s.close()
        


while True:
    run()








# def get_asset_prices():
#     account = Asset.Asset(name, price, quantity)
#     account.view_assets(Asset.assets)