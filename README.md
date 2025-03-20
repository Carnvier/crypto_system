# Crypto Trading Program

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Implementation Plan](#implementation-plan)
- [Running Instructions](#running-instructions)

## Introduction
This report explains the functionality of the Crypto Trading Program, which enables users to engage with the cryptocurrency market by buying, selling, and managing digital assets. It features a user-friendly interface, real-time market data, and tools for portfolio tracking and analysis.

Additionally, I will reflect on my coursework related to this project, discussing the challenges I faced, the skills I developed, and the insights I gained throughout the process.

## Features
- **User-Friendly Interface**: Designed with simplicity in mind, allowing users to navigate effortlessly.
- **Real-Time Market Data**: Access to live cryptocurrency prices and market trends.
- **Portfolio Management**: Users can track their digital assets, monitor performance, and manage trades.
- **Client-Server Architecture**: A robust system that separates client and server responsibilities for enhanced performance.
- **Error Handling**: Built-in mechanisms to manage exceptions and provide user feedback.
- **Graphical Data Visualization**: Utilizes Matplotlib to display market trends and asset performance.

## Implementation Plan
While developing the Crypto Program, I adhered closely to the Coursework Guide. By following the weekly activities step by step, I was able to create a clear plan for structuring the project, as the guide provided well-explained instructions. Additionally, I utilized the "Python Crash Course" by Eric Matthews as a supplementary resource for topics I found unclear, particularly for understanding Matplotlib and data visualization, which proved to be quite beneficial.

In the client-server model, the client is responsible for gathering user input and sending requests to the server. The server processes the client's information, retrieves data from the database, and sends a response back to the client, which then displays the output to the user using the CustomTkinter GUI. 

For instance, in an account management scenario where a user wants to make a deposit, the client collects details such as the username, password, and deposit amount, and sends this information to the server. The server checks the database to verify the user's existence. If the user is found, the server adds the deposit to the user's balance and updates it accordingly. The server then responds with the status of the deposit and the new balance. If the user does not exist, the server sends an error message to the client, which displays the response to the user.

## Running Instructions
Before running this program, several dependencies and modules must be installed to ensure it functions correctly. Most of these dependencies are listed in the `requirements.txt` file located in the same directory as the rest of the code. To install these dependencies, open the terminal, navigate to the directory containing the file, and execute the command:

```bash

pip install -r requirements.txt

This command will install all the necessary requirements.

Once all dependencies have been successfully installed, you can proceed to run the server file from the command line. In the terminal, type:

bash
python server.py

while in the same directory as the server file. Next, open a second terminal in the same directory and enter:

python client.py

The program should start shortly thereafter. To access the account that was used during program development, you may go to the login page and use denzel and 12345 as the username and password respectively (without the quotes).
