import Account, Asset, Portfolio
# from socket import *
# import pickle
# from time import ctime

# HOST = 'localhost'
# PORT = 8080
# ADDRESS = (HOST, PORT)

# s = socket(AF_INET, SOCK_STREAM)
# s.bind(ADDRESS)
# s.listen(1)

# while True:
#     print("...waiting for connection")
#     (client, address) = s.accept()
#     print("Connected with", address)
#     current_time  = ctime()
#     message = f"Hello mate. {current_time}"
#     message = message.encode('ascii')
#     client.send(message)
#     client.close()
#     break


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

def update_account_balance(username, amount, action):
    account = Account.Account(username, password, balance)
    account.update_balance(action, amount)

def process_trade(username, quantity, action):
    process =  Portfolio.Portfolio()
    if action.lower().startswith('b'):
        process.buy_asset(username, asset, quantity)
    elif action.lower().startswith('s'):
        process.sell_asset(username, asset, quantity)
    process.save_transaction(username, asset, quantity, action)

def get_asset_prices():
    account = Asset.Asset(name, price, quantity)
    account.view_assets(Asset.assets)