# import socket
# import time

# PORT = 5050
# SERVER = "10.10.54.156"
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"


# def connect():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR)
#     return client


# def send(client, msg):
#     message = msg.encode(FORMAT)
#     client.send(message)


# def start():
#     answer = input('Would you like to connect (yes/no)? ')
#     if answer.lower() != 'yes':
#         return

#     connection = connect()
#     while True:
#         msg = input("Message (q for quit): ")

#         if msg == 'q':
#             break

#         send(connection, msg)

#     send(connection, DISCONNECT_MESSAGE)
#     time.sleep(1)
#     print('Disconnected')


# start()
import socket
import time
from datetime import datetime

# Server configuration
PORT = 5051

SERVER = "localhost"  
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Function to establish a connection to the server
def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

# Function to send a message to the server
def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

# Function to start the client
def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    # Connect to the server
    connection = connect()

    # Prompt for the username
    username = input("Enter your username: ")
    send(connection, username)  # Send username to the server

    while True:
        msg = input("Message (type 'q' to quit): ")

        if msg.lower() == 'q':
            break
        
        # Prevent sending empty messages
        if msg.strip() == "":
            print("You cannot send an empty message.")
            continue

        # Add a timestamp to the message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {username}: {msg}"
        
        # Send the message to the server
        send(connection, formatted_message)

    # Send a disconnect message before closing the connection
    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)  # Wait for the message to be sent
    print('Disconnected from server.')

# Start the client interaction
start()
