import getpass
from datetime import datetime

assets = {
    "Bitcoin" : 72000,
    "Ethereum" : 27000,
    "Gold": 28000,
    "Silver": 20000,
}

portfolio = {}

def create_account():      
        
    username = getpass.getpass("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")
    initial_deposit = float(getpass.getpass("Please enter your initial deposit: "))

    with open("accounts.txt", "a") as f:
        f.write(f"{username}, \t{password}, \t{initial_deposit}\n")

    print(f"Welcome {username}! You have a current balance of {initial_deposit}.")

def deposit_withdraw(username, amount, action):
    amount = float(amount)
    with open("accounts.txt", "r") as f:
        existing_data = f.readlines()
        for i, line in enumerate(existing_data):
            if username in line:
                username, password, initial_deposit = line.split(',')
                initial_deposit = float(initial_deposit)
                if action.lower() == 'withdraw':
                    if amount > initial_deposit:
                        print("Withdrawal failed insufficient funds!!!")
                    else:
                        initial_deposit = initial_deposit - amount
                        existing_data[i] = f"{username}, \t{password}, \t{initial_deposit}"
                        print(f"Withdrawal of {amount} successful! Your new balance is {initial_deposit}.")
                elif action.lower() == 'deposit':
                    initial_deposit = initial_deposit + amount
                    existing_data[i] = f"{username}, \t{password}, \t{initial_deposit}"
                    print(f"Deposit of {amount} successful! Your new balance is {initial_deposit}.")   
                else:
                    print(f"{action.title()} not found!")                  
    with open("accounts.txt", "w") as f:
        for line in existing_data:
            f.write(f'{line}\n') 

def view_assets(assets):
    print("Current assets:")
    for asset, value in assets.items():
        print(f"{asset:<10}: {value}")

def buy_asset(username, asset, quantity):
    global portfolio
    quantity = int(quantity)
    if asset not in assets:
        print("Asset not found in our portfolio.")
        return
    else: 
        asset_value  = assets[asset]
        total_cost = asset_value * quantity
        with open("accounts.txt", "r") as f:
            existing_data = f.readlines()
            for line in existing_data:
                if username in line:
                    username, password, initial_deposit = line.split(",")
                    balance = float(initial_deposit)
                    if balance < total_cost:
                        print("Insufficient funds for purchase.")
                    elif balance >= total_cost:
                        portfolio = {'username': username, 'asset': asset, 'quantity': quantity, 'price': assets[asset], 'total_cost': total_cost}
                        print("Buy Transaction Success!")
                        print("Buy Transaction Summary:")
                        print(f"{portfolio['username']} {portfolio['asset']} {portfolio['quantity']} {portfolio['price']} {portfolio['total_cost']}")
    return portfolio
                        



def sell_asset(username, asset, quantity):
    global portfolio
    if asset not in assets:
        print("Asset not found in our portfolio.")
        return
    else: 
        asset_value  = assets[asset]
        total_cost = asset_value * quantity
        with open("accounts.txt", "r") as f:
            existing_data = f.readlines()
            for line in existing_data:
                if username in line:
                    username, password, initial_deposit = line.split(",")
                    balance = float(initial_deposit)
                    if balance < total_cost:
                        print("Insufficient funds for purchase.")
                    elif balance >= total_cost:
                        portfolio = {'username': username, 'asset': asset, 'quantity': quantity, 'price': assets[asset], 'total_cost': total_cost}
                        print("Buy Transaction Success!")
                        print("Buy Transaction Summary:")
                        print(f"{portfolio['username']} {portfolio['asset']} {portfolio['quantity']} {portfolio['price']} {portfolio['total_cost']}")
    return portfolio

def view_portfolio(username):
    print(f"Portfolio for {username}:")
    print(f"{portfolio['asset']} {portfolio['quantity']} {portfolio['total_cost']}")

def save_transaction(username, asset, quantity, action):
    with open("transactions.txt", "a") as f:
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        f.write(f"{date}, {username}, {action}, {asset}, {quantity}\n")


view_assets(assets)
buy_asset("dnzel", "Bitcoin", "1")
sell_asset("dnzel", "Bitcoin", "1")


