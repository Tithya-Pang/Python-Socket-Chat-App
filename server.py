# import threading
# import socket

# PORT = 5050
# SERVER = "localhost"
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)

# clients = set()
# clients_lock = threading.Lock()


# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} Connected")

#     try:
#         connected = True
#         while connected:
#             msg = conn.recv(1024).decode(FORMAT)
#             if not msg:
#                 break

#             if msg == DISCONNECT_MESSAGE:
#                 connected = False

#             print(f"[{addr}] {msg}")
#             with clients_lock:
#                 for c in clients:
#                     c.sendall(f"[{addr}] {msg}".encode(FORMAT))

#     finally:
#         with clients_lock:
#             clients.remove(conn)

#         conn.close()


# def start():
#     print('[SERVER STARTED]!')
#     server.listen()
#     while True:
#         conn, addr = server.accept()
#         with clients_lock:
#             clients.add(conn)
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()


# start()
import threading
import socket
from datetime import datetime

# Server configuration
PORT = 5051
SERVER = "localhost"  
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Track connected clients and their usernames
clients = set()
client_usernames = {}  # Dictionary to store usernames
clients_lock = threading.Lock()

# Broadcast messages to all connected clients except the sender
def broadcast(message, sender=None):
    with clients_lock:
        for client in clients:
            if client != sender:  # Don't send the message back to the sender
                try:
                    client.sendall(message.encode(FORMAT))
                except:
                    # Remove clients that can't be reached
                    remove_client(client)

# Handle individual client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        # Ask the client for their username
        conn.send("Enter your username: ".encode(FORMAT))
        username = conn.recv(1024).decode(FORMAT)
        with clients_lock:
            client_usernames[conn] = username

        # Notify all clients that a new user has joined
        welcome_message = f"[SERVER] {username} has joined the chat!"
        broadcast(welcome_message)

        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            # Handle disconnection request
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break

            # Format the message with a timestamp and username
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_message = f"[{timestamp}] {username}: {msg}"
            print(formatted_message)
            broadcast(formatted_message, sender=conn)

    except Exception as e:
        print(f"[ERROR] Exception with {addr}: {e}")

    finally:
        # Handle client disconnection
        remove_client(conn)

# Remove a client from the server and notify others
def remove_client(conn):
    with clients_lock:
        if conn in clients:
            username = client_usernames.get(conn, "Unknown")
            clients.remove(conn)
            disconnect_message = f"[SERVER] {username} has left the chat."
            print(disconnect_message)
            broadcast(disconnect_message)
            conn.close()

# Start the server and listen for connections
def start():
    print("[SERVER STARTED]! Waiting for connections...")
    server.listen()

    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        
        # Start a new thread to handle the client's connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Start the server
start()
