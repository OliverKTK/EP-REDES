# THIS SERVER ACCEPTS MORE THAN ONE CLIENT
# MESSAGES ARE EXCHANGED BETWEEN SERVER AND MULTIPLE CLIENTS
# IT USES MULTITHREADING TO DEAL WITH MULTIPLE CLIENTS

import socket
import threading

HEADER = 64
port = 5000

server = socket.gethostname()
print("Server: " + server)

address = (server, port) # bind to socket
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == "DISCONNECT":
                connected = False
            print(f"[{addr}] {msg}")
        conn.send("Message received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()