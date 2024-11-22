import socket, pickle
import account, asset

def load_accounts():
    with open('accounts.txt', 'r') as f:
        data = f.readlines()
    return data

def load_portfolios():
    with open('portfolio.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            username, action, asset, quantity, total = line.split()
            portfolio = {
                username:{
                    action: {
                        asset: {
                            'quantity': quantity,
                            'total': total
                        }
                    }
                }
            }
    return portfolio

HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 4024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

s.listen(1)



client, address = s.accept()
message = client.recv(BUFSIZE)
# print(message.decode('utf-8'))


# if message.decode('utf-8') == 'signup':
#     message = client.recv(BUFSIZE)
#     user_name, password, balance = message.decode('utf-8').split(',')
#     user = account.Account(user_name.lower().strip(), password.lower().strip(), balance.lower().strip())
#     user.create_account()
#     response = f'success'
#     client.send(response.encode('utf-8'))

# elif message.decode('utf-8') == 'login':
#     message = client.recv(BUFSIZE)
#     user_name, password = message.decode('utf-8').split(',')
#     accounts = load_accounts()
#     login = False
#     for line in accounts:
#         username, passkey, balance,  = line.split(',')
#         if username.lower().strip() == user_name.lower().strip() and passkey.lower().strip() == password.lower().strip():
#             response = f'Success'
#             client.send(response.encode('utf-8'))
#             response = f'{balance}'
#             client.send(response.encode('utf-8'))
#             login = True
    
#     if not login:
#         response = 'Fail'
#         client.send(response.encode('utf-8'))


def run():
    message = client.recv(BUFSIZE)
    message =message.decode('utf-8')
    print(message)
    if message == '1':
        current_assets =  {
        "Bitcoin" : 72000,
        "Ethereum" : 27000,
        "Gold": 28000,
        "Silver": 20000,
        }
        print(current_assets)
        client.sendall(current_assets.encode("utf-8"))
    else: 
        print('error')

run()


# def update_account_balance(username, amount, action):
#     account = Account.Account(username, password, balance)
#     account.update_balance(action, amount)

# def process_trade(username, quantity, action):
#     process =  Portfolio.Portfolio()
#     if action.lower().startswith('b'):
#         process.buy_asset(username, asset, quantity)
#     elif action.lower().startswith('s'):
#         process.sell_asset(username, asset, quantity)
#     process.save_transaction(username, asset, quantity, action)

# def get_asset_prices():
#     account = Asset.Asset(name, price, quantity)
    # account.view_assets(Asset.assets)