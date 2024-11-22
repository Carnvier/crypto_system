import getpass

class Account():

    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def create_account(self):      
        with open("accounts.txt", "a") as f:
            f.write(f"{self.username}, {self.password}, {self.balance}\n")
            f.truncate()
        print(f"Welcome {self.username}! You have a current balance of {self.balance}.")
        return self.username, self.password, self.balance
        
    def deposit(self, amount, existing_data, i):
        self.balance = self.balance + amount
        data = f"{self.username},{self.password},{self.balance}\n"
        existing_data[i] = data
        print(f"Deposit of {amount} successful! Your new balance is {self.balance}.")

    def withdraw(self, amount, existing_data, i):
        if amount > self.balance:
            print("Withdrawal failed insufficient funds!!!")

        self.balance = self.balance - amount
        data = f"{self.username},{self.password},{self.balance}\n"
        existing_data[i] = data
        print(f"Withdrawal of {amount} successful! Your new balance is {self.balance}.")

    def update_balance(self, action, amount):      
        with open("accounts.txt", "r") as f:
            existing_data = f.readlines()
        for i, line in enumerate(existing_data):
            if not self.username in line:
                continue

            user_found = True
            username, password, initial_deposit = line.split(',')
            initial_deposit = float(initial_deposit)
            if action.lower().startswith('d'):
                balance = self.deposit(amount, existing_data, i)
            elif action.lower().startswith('w'):
                balance = self.withdraw(amount, existing_data, i)
            else:
                print(f"{action.title()} not found!")    

        with open("accounts.txt", "w") as f:
            f.seek(0)
            f.writelines(existing_data) 
            f.truncate()
        return balance
                      

                        

# ADD ERROR HANDLING LINES AND COMMENTS