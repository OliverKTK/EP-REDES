import socket

HEADER = 64
port = 5000
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.gethostbyname(socket.gethostname())

address = (server, port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Officially connecting to the server.
client.connect(address)

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World")
input()
send("Hello Matt")
input()
send("Hello Everyone")
input()
send(DISCONNECT_MESSAGE)