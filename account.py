class Account():

    def __init__(self, username, password, balance):
        self.username = username
        self.password = password
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")
        with ("accounts.txt", "r") as f:
                exiting_data = f.readlines()
        with open("accounts.txt", "w") as f:
            for i, line in enumerate(exiting_data):
                if self.username in line:
                    exiting_data[i] = (f"{self.username},{self.password},{self.balance}\n")
            for line in exiting_data:
                f.writelines(line)

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
            with ("accounts.txt", "r") as f:
                exiting_data = f.readlines()
            with open("accounts.txt", "w") as f:
                for i, line in enumerate(exiting_data):
                    if self.username in line:
                        exiting_data[i] = (f"{self.username},{self.password},{self.balance}\n")
                for line in exiting_data:
                    f.writelines(line)

                        

            