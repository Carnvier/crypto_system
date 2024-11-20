import os
from datetime import datetime
import Asset

assets = Asset.assets
class Portfolio():
    def __init__(self):
        self.portfolio = {}

    if not os.path.exists('portfolio.txt'):
        with open('portfolio.txt', 'w') as p:
            p.write("")

    def close_position(self, username, asset, action):
        profit = 0
        user_found = False
        asset_found = False

        with open('portfolio.txt', 'r+') as p:
            existing_data = p.readlines()

            for i, line in enumerate(existing_data):
                user_name, i_action, holding, quantity, cost =  line.split(',')
                quantity, cost = float(quantity), float(cost)
                if username != user_name.strip() or action.lower() != i_action.strip().lower():
                    continue

                user_found = True
                if asset != holding.strip():
                    continue
                asset_found = True

                if i_action.strip().lower().startswith('b'):
                    current_cost = quantity * Asset.assets[asset]
                    profit = current_cost - cost                    
                elif i_action.strip().lower().startswith('s'):
                    current_cost = quantity * Asset.assets[asset]
                    profit = cost - current_cost
                else:
                    print("Action not found")
                    break

                total_earnings = cost + profit                
                existing_data.remove(line)
                print(f"Removed {asset.title()} from your portfolio.")
                break


            p.seek(0)
            p.writelines(existing_data)
            p.truncate()

            with open('accounts.txt', 'r+') as f:
                existing_data = f.readlines()
                for i, line in enumerate(existing_data):
                    user_name, password, balance =  line.split(',')
                    if username != user_name.strip():
                        continue

                    user_found = True
                    balance = float(balance)

                    if user_found and profit > 0:
                        print(f'Profit: {profit}')
                        balance += total_earnings
                        print(f"Updated balance: {balance}")
                        existing_data[i] = f"{user_name},{password}, {balance}\n"
                    
                    if user_found and profit < 0:
                        print(f'Loss: {abs(profit)}')
                        balance -= abs(profit)
                        print(f"Updated balance: {balance}")
                        existing_data[i] = f"{user_name},{password}, {balance}\n"
                
                f.seek(0)
                f.writelines(existing_data)
                f.truncate()       



    def view_holdings(self, username):
        with open('portfolio.txt', "r") as f:
            existing_data = f.readlines()

        print(f"Portfolio for {username}:")
        for line in existing_data:
            user_name, action, asset, quantity, cost = line.split(",")
            if username != user_name.strip():
                continue

            print(f"{action.upper():<10} {asset:<10} {quantity:<10} {cost}", end="")
    
    def buy_asset(self, username, asset, quantity):
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
                            self.portfolio= {
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
                        self.portfolio = {
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
                    existing_data[i] = f"{username.strip()}, \t{password.strip()}, \t{balance}\n"
                    with open("accounts.txt", "w") as f:
                        f.writelines(existing_data) 

                    print(f"Buy Transaction Success!\nCurrent Balance: {balance}\n")
                    print(f"{username.title()} Buy Transaction Summary:")
                    print (f"{asset} {quantity} {asset_value} {total_cost}")
                    return self.portfolio
                        
            if not user_found:
                print(f"{username.title()} not found!")
            return self.portfolio
                        



    def sell_asset(self, username, asset, quantity):
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
                            self.portfolio= {
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
                        self.portfolio = {
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
                    return self.portfolio
                        
            if not user_found:
                print(f"{username.title()} not found!")
            return self.portfolio

    def save_transaction(self, username, asset, quantity, action):
        with open("transactions.txt", "a") as f:
            date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            f.write(f"{date}, {username}, {action}, {asset}, {quantity}\n")

