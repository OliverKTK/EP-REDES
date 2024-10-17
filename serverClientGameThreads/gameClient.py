# PEER TO PEER
# CLIENT PEER

import socket
import time
import threading

from serverClientGame import gameLibrary as g

clientMatch:g.match = None
QUIT:bool = False

def deadMansTrigger(): ## deadMansTrigger() function
    totalWaitTime = 0
    while totalWaitTime < 60:
        totalWaitTime+=1
        time.sleep(1)
    return True

def handleCommand(command, connection):
    global clientMatch
    global QUIT
    if "SHOWBOARD" in command:
        g.showBoard(clientMatch)
    if "INITMATCH" in command:
        temp = command.split(" ")
        scores = [temp[-3], temp[-2], temp[-1]]
        clientMatch = g.match(temp[1], temp[2], temp[3], temp[4], scores)
    if "ASKPLAY" in command:
        deadMansThread = threading.Thread(target=deadMansTrigger)
        deadMansThread.start()
        col = g.playerInput(2, clientMatch)
        deadMansThread.join()
        row = g.addPiece(2, col, clientMatch)
        connection.send(f"{col}".encode())
    if "REMOTEPLAY" in command:
        col = command.split(" ")[-1]
        row = g.addPiece(1, int(col), clientMatch)
    if "NOTICE" in command:
        msg = command.split(':')[1]
        print(msg)
    if "REPLAY" in command:
        valid = True;
        while valid:
            replay = input("Replay?(y/n): ").lower()
            if replay == "n":
                valid = False
                connection.send('n'.encode())
            elif replay == "y":
                valid = False
                connection.send('y'.encode())
    if "QUIT" in command:
        QUIT = True


def clienteProgram():

    host = input("Host: ")
    port = int(input("Port: "))

    clientSocket = socket.socket() # instantiate
    clientSocket.connect((host, port)) # connect to server

    global QUIT

    nomeServidor = clientSocket.recv(1024).decode() # gets server name (p1)
    print(f"Connected to [{nomeServidor}]")

    nomeCliente = input('Player name: ').lower() # gets client name (p2)
    clientSocket.send(nomeCliente.encode())

    print(f"Waiting for [{nomeServidor}]'s character selection...")
    charP1 = clientSocket.recv(1024).decode() # pega o char de p1
    print(f"[{nomeServidor}] chose the character [{charP1}]")

    charP2 = " " # pega o char de p2
    while charP2 == " " or charP2.lower() == charP1.lower() or len(charP2) > 1:
        if charP2.lower() == charP1.lower():
            print("Choose a different character")
        elif len(charP2) > 1:
            print("Choose only one character")
        charP2 = input(f"{nomeCliente} character: ")
    clientSocket.send(charP2.encode())

    while not QUIT:
        command = clientSocket.recv(1024).decode() # receives instruction
        handleCommand(command, clientSocket) # passes the instruction to the handler

    clientSocket.close() # close the connection

if __name__ == '__main__':
    clientThread = threading.Thread(target=clientProgram)