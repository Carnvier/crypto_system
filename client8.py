from socket import *
import pickle
import account, asset, portfolio

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






def add_funds(amount):
    message = f"deposit funds, {amount}"
    message = message.encode("utf-8")
    (server, address) = s.accept()
    server.send(message)

            

def withdraw_funds(amount):
    message = f"withdraw funds, {amount}"
    message = message.encode("utf-8")
    (server, address) = s.accept()
    server.send(message)

def execute_trade(asset, quantity, action):
    message = f"{asset}, {quantity}, {action}"
    message = message.encode("utf-8")
    (server, address) = s.accept()
    server.send(message)

def view_portfolio():
    message = f"view portfolio"
    message = message.encode("utf-8")
    (server, address) = s.accept()
    server.send(message)


