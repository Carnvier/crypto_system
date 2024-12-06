from customtkinter import *
from PIL import Image, Image
import asset as ast



# Create a new window
app = CTk()
app.title = "CryptoHive Trading Platform"
app.geometry("1000x650+0+0")


def start_window():
    title = CTkLabel(master=app, text="CryptoHive Trading Platform", font=("Helvetica", 37), text_color="gold")
    title.place(relx=0.75, rely=0.3, anchor="center")

    slogan = CTkLabel(master=app, text="Buzzing Towards Financial Freedom.", font=("Helvetica", 22))
    slogan.place(relx=0.75, rely=0.37, anchor="center")

    description = CTkLabel(master=app, text="Login or signup.", font=("Helvetica", 19), text_color="gold")
    description.place(relx=0.75, rely=0.47, anchor="center")

    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20), command=login)
    login_button.place(relx=0.75, rely=0.55, anchor="center")

    signup_button = CTkButton(master=app, text="Sign Up", font=("Helvetica", 20), command=signup)
    signup_button.place(relx=0.75, rely=0.65, anchor="center")

def login():
    title = CTkLabel(master=app, text="Login", font=("Helvetica", 45))
    title.place(relx=0.5, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.35, rely=0.4, anchor="center")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.5, rely=0.4, anchor="center")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.35, rely=0.5, anchor="center")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.5, rely=0.5, anchor="center")
    
    login_button = CTkButton(master=app, text="Login", font=("Helvetica", 20),)
    login_button.place(relx=0.5, rely=0.6, anchor="center")

def signup():
    title = CTkLabel(master=app, text="Signup", font=("Helvetica", 45))
    title.place(relx=0.5, rely=0.3, anchor="center")
    
    username_label = CTkLabel(master=app, text="Username:", font=("Helvetica", 20))
    username_label.place(relx=0.35, rely=0.4, anchor="w")

    username_entry = CTkEntry(master=app)
    username_entry.place(relx=0.69, rely=0.4, anchor="e")

    password_label = CTkLabel(master=app, text="Password:", font=("Helvetica", 20))
    password_label.place(relx=0.35, rely=0.5, anchor="w")
    
    password_entry = CTkEntry(master=app, show="*")
    password_entry.place(relx=0.69, rely=0.5, anchor="e")

    confirm_password_label = CTkLabel(master=app, text="Confirm Password:", font=("Helvetica", 20))
    confirm_password_label.place(relx=0.35, rely=0.6, anchor="w")
    
    confirm_password_entry = CTkEntry(master=app, show="*")
    confirm_password_entry.place(relx=0.69, rely=0.6, anchor="e")

    initial_deposit_label = CTkLabel(master=app, text="Initial Deposit:", font=("Helvetica", 20))
    initial_deposit_label.place(relx=0.35, rely=0.7, anchor="w")
    
    initial_deposit_entry = CTkEntry(master=app, validate="key", validatecommand=(app.register(validate_initial_deposit), "%P"))
    initial_deposit_entry.place(relx=0.69, rely=0.7, anchor="e")
    
    
    signup_button = CTkButton(master=app, text="Signup", font=("Helvetica", 20),)
    signup_button.place(relx=0.5, rely=0.8, anchor="center")

def validate_initial_deposit(value):
    if value == "":
        return True  
    try:
        float(value)  
        return True  
    except ValueError:
        return False  

def login_confirmation():
    login_confirm = CTkLabel(master=app, text="Login Successful", font=("Helvetica", 45), text_color="gold")
    login_confirm.place(relx=0.5, rely=0.3, anchor="center")
    username = "Denzel"
    welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
    welcome_msg.place(relx=0.5, rely=0.45, anchor="center")

    balance = -2000  # Replace with actual balance

    if balance > 0:
        color = "green"
    else:
        color = "red"

    balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance}", font=("Helvetica",30), text_color=color)
    balance_label.place(relx=0.5, rely=0.6, anchor="center")

def signup_confirmation():
    signup_confirmed = CTkLabel(master=app, text="Signup Successful", font=("Helvetica", 45), text_color="gold")
    signup_confirmed.place(relx=0.5, rely=0.3, anchor="center")
    username = "Denzel"
    welcome_msg = CTkLabel(master=app, text=f"Welcome {username}", font=("Helvetica", 35))
    welcome_msg.place(relx=0.5, rely=0.45, anchor="center")

    balance = -2000  # Replace with actual balance

    if balance > 0:
        color = "green"
    else:
        color = "red"

    balance_label = CTkLabel(master=app, text=f"Your current balance: ${balance}", font=("Helvetica",30), text_color=color)
    balance_label.place(relx=0.5, rely=0.6, anchor="center")



asset_frame = CTkFrame(master=app, fg_color='black', border_color="white", border_width=1, )
asset_frame.place(relx=-0.01, rely=-0.01, relwidth=0.25, relheight=1.02)

title = CTkLabel(asset_frame, text="Assets", text_color="white", font=("Helvetica", 25))
title.place(relx=0.5, rely=0.1, anchor="center")
assets = ast.Asset().get_values()
y = 0.2

for asset, value in assets.items():
    asset_label = CTkLabel(asset_frame, text=f"{asset}", text_color="white", font=("Helvetica", 15))
    asset_label.place(relx=0.1, rely=y, anchor="w")
    graph_button = CTkButton(asset_frame, text=f"{value:.2f}", fg_color="darkblue", font=("Helvetica", 15), width = 100, border_width=1, border_color="white")
    graph_button.place(relx=0.9, rely=y, anchor="e")
    y += 0.06

graph_frame = CTkFrame(master=app, fg_color="#B8860B")
graph_frame.place(relx=0.25, rely=0.0, relwidth=0.8, relheight=1.02)

graph =
   


app.mainloop()