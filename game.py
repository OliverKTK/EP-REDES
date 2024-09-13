import numpy as np
import random as rd

QUIT = False; GAME = True
PLAYER1 = 1; PLAYER2 = 2
HEIGHT = 6; WIDTH = 7
NUMFORWIN = 4
empitySpaces = HEIGHT*WIDTH


def showBoard():
    for i in range(0, HEIGHT):
        print("")
        for j in range(0, WIDTH):
            if board[i][j] == 0:
                print("| |", end="")
            elif board[i][j] == 1:
                print(f"|{charP1}|", end="")
            else:
                print(f"|{charP2}|",end="")
    print("")
    for i in range(0, WIDTH):
        print(f"|{i+1}|", end="")
    print("")
    
def playerInput(player: int):
    retry = True
    col = -1
    if player == 1:
        char = charP1
    else:
        char = charP2
    while retry:
        try:
            col = int(input(f"Player {player} place a piece({char}): ")) -1
            while col<0 or col>WIDTH:
                print(f"Choose a number between 1 and {WIDTH}")
                col = int(input(f"Player {player} place a piece({char}): ")) -1
            return col 
        except ValueError:
            print("Please enter a number")

def addPiece(player: int, col: int):
    # add piece to free row and return the number of the row
    retry = True
    while retry:
        if board[0][col] != 0:
            print("Cant place there")
            col = playerInput(player)
        else:
            retry = False
            for i in range(0, HEIGHT):
                if board[5-i][col] == 0:
                    board[5-i][col] = player
                    return 5-i
            
def checkVertical(player: int, row: int, col: int):
    # teste Vertical se conectado 4 a partir da ultima peca adicionada
    test = True
    tempCol = col; tempRow = row
    connected = 1
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica se as proximas 3 pecas abaixo da ultima adicionada pertence ao mesmo player
        if tempRow + 1 <= HEIGHT -1:
            tempRow += 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        else:
            return False

def checkHorizontal(player: int, row: int, col: int):
    # teste Horizontal se conectado 4 a partir da ultima peca adicionada
    test = True; left = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas a esquerda da ultima adicionada pertencem ao mesmo player 
        if tempCol - 1 >= 0 and left:
            tempCol -= 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                tempCol = col
                left = False
        elif left:
            tempCol = col
            left = False
        # se nao tiver mais pecas a esquerda volta a posicao da ultima adicionada e verifica as pecass a direita
        if tempCol + 1 <= WIDTH -1 and not left:
            tempCol += 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        elif not (tempCol + 1 <= WIDTH -1): 
            return False

def checkDiag1(player: int, row: int, col: int):
    # teste diagonal / se conectado 4 a partir da ultima peca colocada
    test = True; bottomLeft = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas na diagona(/) esquerda perntencem ao player
        if tempCol - 1 >= 0 and tempRow + 1 <= HEIGHT -1 and bottomLeft:
            tempCol -= 1; tempRow += 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                tempCol = col; tempRow = row
                bottomLeft = False
        elif bottomLeft:
            tempCol = col; tempRow = row
            bottomLeft = False
        # se nao tiver mais pecas na diagonal(/) esqueda verifica as da diagonal(/) direita  
        if tempCol + 1 <= WIDTH -1 and tempRow - 1 >= 0 and not bottomLeft:
            tempCol += 1; tempRow -= 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False 
        elif not (tempCol + 1 <= WIDTH -1 and tempRow - 1 >= 0):
            return False
        
def checkDiag2(player: int, row: int, col: int):
    # teste diagonal \ se conectado 4 a partir da ultima peca colocada
    test = True; uppperLeft = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas na diagona(\) esquerda perntencem ao player
        if tempCol - 1 >= 0 and tempRow - 1 >= 0 and uppperLeft:
            tempCol -= 1; tempRow -= 1
            if board[tempRow][tempCol] == player:
                connected += 1  
            else:
                tempCol = col; tempRow = row
                uppperLeft = False
        elif uppperLeft:
            tempCol = col; tempRow = row
            uppperLeft = False
        # se nao tiver mais pecas na diagonal(\) esqueda verifica as da diagonal(\) direita 
        if tempCol + 1 <= WIDTH -1 and tempRow + 1 <= HEIGHT -1 and not uppperLeft:  
            tempCol += 1; tempRow += 1
            if board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        elif not (tempCol + 1 <= WIDTH -1 and tempRow + 1 <= HEIGHT -1):
            return False

def checkWin(player: int, row: int, col: int):
    # verifica se o player ganhou ou se ocorreu um empate
    global empitySpaces
    if empitySpaces <= 0:
        return -1
    else:
        empitySpaces -= 1
        if checkVertical(player, row, col) or checkHorizontal(player, row, col) or checkDiag1(player, row, col) or checkDiag2(player, row, col):
            if player == PLAYER1:
                return 1
            elif player == PLAYER2:
                return 2

#while loop se continua com jogos novos
while not QUIT: 
    board = np.zeros((HEIGHT,WIDTH))

    # board for tests
    # board = [[0,0,0,0,0,0,0],
    #          [0,0,0,0,0,0,0],
    #          [0,0,0,0,0,0,0],
    #          [0,0,0,0,0,0,0],
    #          [0,0,0,0,0,0,0],
    #          [0,0,0,0,0,0,0],]

    charP1 = " "
    while charP1 == " " or len(charP1) > 1:
        if len(charP1) > 1:
            print("Choose only one character")
        charP1 = input("Player 1 character: ")

    charP2 = " "
    while charP2 == " " or charP2.lower() == charP1.lower() or len(charP2) > 1:
        if charP2.lower() == charP1.lower():
            print("Choose a diffrent character")
        elif len(charP2) > 1:
            print("Choose only one character")
        charP2 = input("Player 2 character: ")

    # decide qual player faz a primeira jogada
    if rd.random() <= 0.5:
        turnP1 = True
        print("Player 1 Starts")
        
    else:
        turnP1 = False
        print("Player 2 Starts")

    showBoard()
    # while loop do jogo que esta ocorrendo
    while GAME:
        if turnP1:
            col = playerInput(PLAYER1)
            row = addPiece(PLAYER1, col)
            result = checkWin(PLAYER1, row, col)
            turnP1 = False
        else:
            col = playerInput(PLAYER2)
            row = addPiece(PLAYER2, col)
            result = checkWin(PLAYER2, row, col)
            turnP1 = True
            
        showBoard()
        if result == 1 or result == 2:
            print(f"Player {result} Wins")
            GAME = False
        elif result == -1:
            print("Draw")
            GAME = False
    valid = True
    while valid:
        replay= input("Replay?(y/n): ").lower()
        if replay == "n":
            valid = False
            QUIT = True
        elif replay == "y":
            valid = False
            
