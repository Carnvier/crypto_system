import socket, pickle
import time


HOST = 'localhost'
PORT = 3030
ADDRESS = (HOST, PORT)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def run():
    # display_account()
    while True:
        print("Welcome to the Menu")
        print("1. View Asset")
        option = input("Select the option from the list above using the number.")
        if option == '1':
            view_assets()

def display_account():
    print("*"*10, "Welcome to DGTraders", "*"*10 )
    account = input("Do you have an account? (y/n): ")
    if account.lower().startswith("n"):
        print("Lets get you started...")
        message = "signup"
        s.send(message.encode("utf-8"))
        user_name = input("Please enter your username: ")
        while True:
            password = input("Please enter your password: ")
            confirm_password = input("Please re-enter your password: ")
            if confirm_password == password:
                break
            if confirm_password != password:
                print("Passwords do not match!")
                continue
        deposit = input("Please enter your deposit: ")

        message = f"{user_name}, {password}, {deposit}"
        s.send(message.encode("utf-8"))
        response = s.recv(BUFSIZE)
        if response.decode() == "success":
            print("Account successfully created") 
        else:
            print("Error creating account. Please contact administrator")       

    elif account.lower().startswith("y"):    
        message = f'login'
        s.send(message.encode('utf-8'))
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        message = f'{user_name}, {password}'
        s.send(message.encode('utf-8'))
        response = s.recv(BUFSIZE)
        if response.decode('utf-8').lower() == 'success':
            balance = s.recv(BUFSIZE)
            balance = float(balance.decode('utf-8'))
            print(f'Your current balance: {balance:.2f}')
        elif response.decode('utf-8').lower() == 'fail':
            print('Your password of username is incorrect. Please try again')
        return

def view_assets():
    message = "1"
    s.send(message.encode('utf-8'))
    assets = s.recv(BUFSIZE)
    assets = assets.decode('utf-8')
    print("Current assets:")
    for asset, value in assets.items():
        print(f"{asset:<10}: {value}")

while True:
    s.connect(ADDRESS)
    print('Connected to server')
    run()
    s.close()
    break

