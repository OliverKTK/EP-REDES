# THIS SERVER ONLY ACCEPTS ONE CLIENT
# THE MESSAGES ARE EXCHANGED ONLY BETWEEN SERVER AND CLIENT

import socket

import gameLibrary as g

def serverProgram():
    # get hostname
    host=socket.gethostname()
    port = 5000 # acho que dá pra deixar pro usuário escolher depois, mas por hora é isso aqui mesmo
                # não iniciar com qualquer port abaixo de 1024 (são reservadas)

    serverSocket = socket.socket() #get instance
    serverSocket.bind((host, port))

    # configure how many clients can listen simultaneously (2)
    serverSocket.listen(4)

    nomeServidor = input("Nome do jogador: ") # pega o nome do servidor (p1)

    conn, address = serverSocket.accept() # accept new connection
    conn.send(nomeServidor.encode())

    nomeCliente = conn.recv(1024).decode() # pega o nome do cliente (p2)
    print(f"[{nomeCliente}] connection from {str(address)}")

    charP1 = " " # pega o char de p1
    while charP1 == " " or len(charP1) > 1:
        if len(charP1) > 1:
            print("Choose only one character")
        charP1 = input("Player 1 character: ")
    conn.send(charP1.encode())

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
        turn = g.gameStarter()
        if turn == 1:
            turnP1 = True
            print(f"[{nomeServidor}] starts")
        else:
            turnP1 = False
            conn.send("ASKPLAY".encode())
        g.showBoard(currentMatch)
        conn.send("SHOWBOARD".encode())
        while GAME:
            currentMatch.scores[0] += 1
            if turnP1:
                col = g.playerInput(PLAYER1, currentMatch)
                row = g.addPiece(PLAYER1, col, currentMatch)
                result = g.checkWin(PLAYER1, row, col, currentMatch)
                turnP1 = False
            else:
                col = g.playerInput(PLAYER2, currentMatch)
                row = g.addPiece(PLAYER2, col, currentMatch)
                result = g.checkWin(PLAYER2, row, col, currentMatch)
                turnP1 = True

            g.showBoard(currentMatch)
            if result == 1 or result == 2:
                print(f"Player {result} Wins")
                currentMatch.scores[PLAYER1] += 1
                GAME = False
            elif result == -1:
                print("Draw")
                currentMatch.scores[PLAYER2] += 1
                GAME = False
        valid = True
        while valid:
            replay = input("Replay?(y/n): ").lower()
            if replay == "n":
                valid = False
                QUIT = True
            elif replay == "y":
                valid = False
                GAME = True

    conn.close() # close the connection

if __name__ == '__main__':
    serverProgram()
