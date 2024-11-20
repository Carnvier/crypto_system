from socket import *
import pickle
import Account, Asset, Portfolio

HOST = 'localhost'
PORT = 8080
ADDRESS = (HOST, PORT)

BUFSIZE = 1024

s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDRESS)
message = s.recv(BUFSIZE)
print(f'Server sent the following')
print(message.decode('ascii'))
s.close()

def display_account():
    user_name = input("Please enter your username: ")
    password = input("Please enter your password: ")
    message = f'{user_name}, {password}'
    message = message.encode('ascii')
    print()

def view_assets():
    pass

def add_funds(amount):
    pass

def withdraw_funds(amount):
    pass

def execute_trade(asset, quantity, action):
    pass

def view_portfolio():
    pass