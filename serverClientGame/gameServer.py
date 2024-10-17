# PEER TO PEER / CLIENT SERVER HYBRID
# SERVER PROGRAM

import socket
import time

from serverClientGame import gameLibrary as g


def serverProgram():
    # get hostname
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)
    host=''
    port = 0
    while port<1024:
        port = int(input('Choose a port: '))


    print(f"Host: [{hostname}]")
    print(f"Port: {port}")

    serverSocket = socket.socket() #get instance
    serverSocket.bind((host, port))

    # configure how many clients can listen simultaneously (1)
    serverSocket.listen(1)

    nomeServidor = input("Player name: ").lower() # gets P1's name

    print('Waiting for a connection...')

    conn, address = serverSocket.accept() # accept new connection
    conn.send(nomeServidor.encode())

    nomeCliente = conn.recv(1024).decode() # gets P2's name
    print(f"[{nomeCliente}] connection from {str(address)}")

    charP1 = " " # gets P1's character
    while charP1 == " " or len(charP1) > 1:
        if len(charP1) > 1:
            print("Choose only one character")
        charP1 = input(f"[{nomeServidor}] character: ")
    conn.send(charP1.encode())

    print(f"Waiting for [{nomeCliente}]'s character selection...")
    charP2 = conn.recv(1024).decode() # gets P2's character
    print(f"[{nomeCliente}] chose the character [{charP2}]")

    QUIT = False; GAME = True
    PLAYER1 = 1; PLAYER2 = 2
    HEIGHT = 6; WIDTH = 7
    NUMFORWIN = 4
    empitySpaces = HEIGHT * WIDTH
    scores=[0, 0, 0]

    while not QUIT: # game loop
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
                time.sleep(0.5)
                col = int(conn.recv(1024).decode())
                row = g.addPiece(2, col, currentMatch) # vai ter que ser repetido em cliente
                result = g.checkWin(2, row, col, currentMatch)
                turnP1 = True

            time.sleep(0.5)
            g.showBoard(currentMatch)
            conn.send("SHOWBOARD".encode())
            time.sleep(0.5)

            if result == 1 or result == 2: # finaliza
                if(result == 1):
                    msg = f'Player [{nomeServidor}] wins!'
                    currentMatch.scores[PLAYER1] += 1
                elif(result == 2):
                    msg = f'Player [{nomeCliente}] wins!'
                    currentMatch.scores[PLAYER2] += 1
                GAME = False
                print(msg)
                conn.send(f'NOTICE:{msg}'.encode())
            elif result == -1:
                msg = 'Draw!'
                currentMatch.scores[PLAYER2] += 1
                GAME = False
                print(msg)
                conn.send(f'NOTICE:{msg}'.encode())
        valid = True
        conn.send('REPLAY'.encode())
        replayClient = conn.recv(1024).decode()
        while valid:
            replayServer = input("Replay?(y/n): ").lower()
            if replayServer == "n" or replayClient == "n":
                if replayServer == 'n' and replayClient == 'y':
                    msg = f'[{nomeServidor}] quit'
                elif replayServer == 'y' and replayClient == 'n':
                    msg = f'[{nomeCliente}] quit'
                elif replayServer == 'n' and replayClient == 'n':
                    msg = f'Quitting game'
                conn.send(f'NOTICE:{msg}'.encode())
                print(f'{msg}')
                time.sleep(0.5)
                conn.send('QUIT'.encode())
                valid = False
                QUIT = True
            elif replayServer == "y" and replayClient == "y":
                valid = False
                GAME = True

    conn.close() # close the connection

if __name__ == '__main__':
    serverProgram()
