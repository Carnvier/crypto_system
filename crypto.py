import getpass, os
from datetime import datetime

assets = {
    "Bitcoin" : 72000,
    "Ethereum" : 27000,
    "Gold": 28000,
    "Silver": 20000,
}

if not os.path.exists('portfolio.txt'):
        with open('portfolio.txt', 'w') as p:
            p.write("")

portfolio = {}

def create_account():      
        
    username = getpass.getpass("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")
    initial_deposit = float(getpass.getpass("Please enter your initial deposit: "))

    with open("accounts.txt", "a") as f:
        f.write(f"{username}, {password}, {initial_deposit}\n")
        f.truncate()


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
                        existing_data[i] = f"{username}, {password}, {initial_deposit}\n"
                        print(f"Withdrawal of {amount} successful! Your new balance is {initial_deposit}.")
                elif action.lower() == 'deposit':
                    initial_deposit = initial_deposit + amount
                    existing_data[i] = f"{username}, {password}, {initial_deposit}\n"
                    print(f"Deposit of {amount} successful! Your new balance is {initial_deposit}.")   
                else:
                    print(f"{action.title()} not found!")                  
    
    with open("accounts.txt", "w") as f:
        f.seek(0)
        for line in existing_data:
            f.writelines(f'{line}') 
        f.truncate()

def view_assets(assets):
    print("Current assets:")
    for asset, value in assets.items():
        print(f"{asset:<10}: {value}")

def buy_asset(username, asset, quantity, portfolio):
    user_found = False
    quantity = int(quantity)
    action = "buy"

    if asset not in assets:
        print("Asset not found in our portfolio.")
        return
    
   
    asset_value  = assets[asset]
    total_cost = asset_value * quantity
    with open("accounts.txt", "r") as f:
        existing_data = f.readlines()

        for i, line in enumerate(existing_data):
            user_name, password, initial_deposit = line.split(",")

            if username != user_name.strip():
                continue

            user_found = True
            balance = float(initial_deposit)
            if balance < total_cost:
                print("Insufficient funds for purchase.")
                return
            
            with open('portfolio.txt', 'r+') as p:
                current_data = p.readlines()
                asset_found = False

                for j, dic in enumerate(current_data):
                    if asset in dic and user_found and action in dic:
                        asset_found = True
                        c_quantity, c_cost = map(float, dic.split(',')[3:5])
                        total_quantity = c_quantity + quantity
                        new_total_cost = c_cost + total_cost
                        portfolio= {
                            username:{
                                action:{
                                    asset:{ 
                                        'quantity': total_quantity,
                                        'total_cost': new_total_cost
                                    }
                                }
                            }
                        }
                        current_data[j] = f"{user_name}, {action}, {asset}, {total_quantity}, {new_total_cost}\n"
                
                if  not asset_found:
                    portfolio = {
                        username : {
                            action:{
                                asset: {
                                    'quantity': quantity, 
                                    'total_cost': total_cost
                                }
                            }
                        }
                    }
                    data = f"{username}, {action}, {asset}, {quantity}, {total_cost}\n"
                    current_data.append(data)
                    print("ichoooooo")

                p.seek(0)
                p.writelines(current_data)
                p.truncate()

                balance = balance - total_cost
                existing_data[i] = f"{username.strip()}, \t{password.strip()}, \t{balance}\n"
                with open("accounts.txt", "w") as f:
                    f.writelines(existing_data) 

                print(f"Buy Transaction Success!\nCurrent Balance: {balance}\n")
                print(f"{username.title()} Buy Transaction Summary:")
                print (f"{asset} {quantity} {asset_value} {total_cost}")
                return portfolio
                    
        if not user_found:
            print(f"{username.title()} not found!")
        return portfolio
                        



def sell_asset(username, asset, quantity, portfolio):
    user_found = False
    quantity = int(quantity)
    action = "sell"

    if asset not in assets:
        print("Asset not found in our portfolio.")
        return
     
    asset_value  = assets[asset]
    total_cost = asset_value * quantity
    with open("accounts.txt", "r") as f:
        existing_data = f.readlines()

        for i, line in enumerate(existing_data):
            user_name, password, initial_deposit = line.split(",")

            if username != user_name.strip():
                continue
            
            user_found = True
            balance = float(initial_deposit)
            if balance < total_cost:
                print("Insufficient funds for purchase.")
                return
            
                    
            with open('portfolio.txt', 'r+') as p:
                current_data = p.readlines()
                asset_found = False

                for j, dic in enumerate(current_data):
                    if asset in dic and user_found and action in dic:
                        asset_found = True
                        c_quantity, c_cost = map(float, dic.split(',')[3:5])
                        total_quantity = c_quantity + quantity
                        new_total_cost = c_cost + total_cost
                        portfolio= {
                            username:{
                                action:{
                                    asset: {
                                        'quantity': total_quantity,
                                        'total_cost': new_total_cost
                                    }
                                }
                            }
                        }
                        current_data[j] = f"{user_name}, {action}, {asset}, {total_quantity}, {new_total_cost}\n"

                if not asset_found and user_found :
                    portfolio = {
                        username : {
                            action:{
                                asset: {
                                    'quantity': quantity, 
                                    'total_cost': total_cost
                                }
                            }
                        }
                    }
                    data = f"{username}, {action}, {asset}, {quantity}, {total_cost}\n"
                    current_data.append(data)
                    
                            
                p.seek(0)
                p.writelines(current_data)
                p.truncate()

                balance = balance - total_cost
                existing_data[i] = f"{username.strip()}, {password.strip()}, {balance}\n"
                with open("accounts.txt", "w") as f:
                    f.writelines(existing_data) 

                print(f"Sell Transaction Success!\nCurrent Balance: {balance}\n")
                print(f"{username.title()} Sell Transaction Summary:")
                print (f"{asset} {quantity} {asset_value} {total_cost}")
                return portfolio
                    
        if not user_found:
            print(f"{username.title()} not found!")
        return portfolio

def view_portfolio(username, portfolio):
    with open('portfolio.txt', "r") as f:
        existing_data = f.readlines()

    print(f"Portfolio for {username}:")
    for line in existing_data:
        user_name, action, asset, quantity, cost = line.split(",")
        if username != user_name.strip():
            continue

        print(f"{action.upper():<10} {asset:<10} {quantity:<10} {cost}", end="")
        

def save_transaction(username, asset, quantity, action):
    with open("transactions.txt", "a") as f:
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        f.write(f"{date}, {username}, {action}, {asset}, {quantity}\n")



view_assets(assets)
sell_asset("cocinito", "Silver", "4", portfolio)
# sell_asset("cocinito", "Gold", "2", portfolio)
view_portfolio("cocinito", portfolio)
save_transaction("cocinito", "Gold", "4", "sell")


