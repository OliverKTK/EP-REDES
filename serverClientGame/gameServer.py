# THIS SERVER ONLY ACCEPTS ONE CLIENT
# THE MESSAGES ARE EXCHANGED ONLY BETWEEN SERVER AND CLIENT

import socket
import time

import gameLibrary as g

def serverProgram():
    # get hostname
    hostname = socket.gethostname()
    host=socket.gethostbyname(hostname)
    port = 0
    while port<1024:
        port = int(input('Choose a port: '))


    print(f"Host: [{hostname}] on IP address [{host}]")
    print(f"Port: {port}")

    serverSocket = socket.socket() #get instance
    serverSocket.bind((host, port))

    # configure how many clients can listen simultaneously (2)
    serverSocket.listen(4)

    nomeServidor = input("Player name: ") # pega o nome do servidor (p1)

    print('Waiting for a connection...')

    conn, address = serverSocket.accept() # accept new connection
    conn.send(nomeServidor.encode())

    nomeCliente = conn.recv(1024).decode() # pega o nome do cliente (p2)
    print(f"[{nomeCliente}] connection from {str(address)}")

    charP1 = " " # pega o char de p1
    while charP1 == " " or len(charP1) > 1:
        if len(charP1) > 1:
            print("Choose only one character")
        charP1 = input(f"[{nomeServidor}] character: ")
    conn.send(charP1.encode())

    print(f"Waiting for [{nomeCliente}]'s character selection...")
    charP2 = conn.recv(1024).decode() # pega o char de P2
    print(f"[{nomeCliente}] chose the character [{charP2}]")

    QUIT = False; GAME = True
    PLAYER1 = 1; PLAYER2 = 2
    HEIGHT = 6; WIDTH = 7
    NUMFORWIN = 4
    empitySpaces = HEIGHT * WIDTH
    scores=[0, 0, 0]

    while not QUIT:
        currentMatch = g.match(nomeServidor, nomeCliente, charP1, charP2, scores)
        conn.send(f"INITMATCH {nomeServidor} {nomeCliente} {charP1} {charP2} {scores[0]} {scores[1]} {scores[2]}".encode())
        time.sleep(0.5)
        turn = g.gameStarter()
        if turn == 1:
            turnP1 = True
            msg = f"{nomeServidor} starts"
            conn.send(f"NOTICE:{msg}".encode())
            print(msg)
            time.sleep(0.5)
        else:
            turnP1 = False
            msg = f"{nomeCliente} starts"
            conn.send(f"NOTICE:{msg}".encode())
            print(msg)
        g.showBoard(currentMatch)
        conn.send("SHOWBOARD".encode())
        time.sleep(0.5)
        while GAME:
            currentMatch.scores[0] += 1
            if turnP1:
                conn.send(f"NOTICE:Waiting for [{nomeServidor}]...".encode())
                col = g.playerInput(1, currentMatch)
                time.sleep(0.5)
                conn.send(f"REMOTEPLAY {col}".encode())
                row = g.addPiece(1, col, currentMatch)
                result = g.checkWin(1, row, col, currentMatch)
                turnP1 = False
            else:
                print(f"Waiting for [{nomeCliente}]...")
                conn.send("ASKPLAY".encode())
                col = int(conn.recv(1024).decode())
                time.sleep(0.5)
                row = g.addPiece(2, col, currentMatch) # vai ter que ser repetido em cliente
                result = g.checkWin(2, row, col, currentMatch)
                turnP1 = True

            g.showBoard(currentMatch)
            conn.send("SHOWBOARD".encode())
            time.sleep(0.5)

            # ADAPTADO ATÉ ESTE PONTO
            if result == 1 or result == 2: # tem que adaptar para exibir o nome do jogador em vez do número
                if(result == 1):
                    msg = f'Player [{nomeServidor}] wins!'
                    currentMatch.scores[PLAYER1] += 1
                elif(result == 2):
                    msg = f'Player [{nomeCliente}] wins!'
                    currentMatch.scores[PLAYER2] += 1
                GAME = False
            elif result == -1:
                msg = 'Draw!'
                currentMatch.scores[PLAYER2] += 1
                GAME = False
            print(msg)
            conn.send(f'{msg}'.encode())
        valid = True
        replayClient = conn.recv(1024).decode()
        time.sleep(0.5)
        while valid:
            conn.send('REPLAY'.encode())
            replayServer = input("Replay?(y/n): ").lower()
            time.sleep(0.5)
            replayClient = conn.recv(1024).decode()
            if replayServer == "n" or replayClient == "n":
                valid = False
                QUIT = True
            elif replayServer == "y" and replayClient == "y":
                valid = False
                GAME = True

    conn.close() # close the connection

if __name__ == '__main__':
    serverProgram()
