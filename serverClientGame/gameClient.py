# THIS CLIENT STRUTURE ONLY WORKS FOR ONE CLIENT

import socket
import gameLibrary as g

clientMatch:g.match = None

def handleCommand(command):
    global clientMatch
    if command == "SHOWBOARD":
        g.showBoard(clientMatch)
    elif "INITMATCH" in command:
        temp = command.split(" ")
        scores = [temp[-3], temp[-2], temp[-1]]
        clientMatch = g.match(temp[1], temp[2], temp[3], temp[4], scores)
    elif command == "ASKPLAY":
        print("recebido pedido de jogada :D")


def clienteProgram():
    host = socket.gethostname() # as both codes are running on the same PC (needs to fix for multiple machines)
    port = 5000 # socket server port number (needs to fic for multiple machines)

    clientSocket = socket.socket() # instanciate
    clientSocket.connect((host, port)) # connect to server

    nomeServidor = clientSocket.recv(1024).decode() # pega o nome do servidor (p1)
    print(f"Connected to [{nomeServidor}]")

    nomeCliente = input('Player name: ') # pega o nome do cliente (p2)
    clientSocket.send(nomeCliente.encode())

    charP1 = clientSocket.recv(1024).decode() # pega o char de p1
    print(f"[{nomeServidor}] chose the character [{charP1}]")

    charP2 = " " # pega o char de p2
    while charP2 == " " or charP2.lower() == charP1.lower() or len(charP2) > 1:
        if charP2.lower() == charP1.lower():
            print("Choose a diffrent character")
        elif len(charP2) > 1:
            print("Choose only one character")
        charP2 = input("Player 2 character: ")
    clientSocket.send(charP2.encode())

    while True:
        command = clientSocket.recv(1024).decode() # recebe alguma instrucao do servidor
        handleCommand(command)

    clientSocket.close() # close the connection

if __name__ == '__main__':
    clienteProgram()