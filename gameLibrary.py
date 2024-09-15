from termcolor import colored
import random as rd

QUIT = False; GAME = True
PLAYER1 = 1; PLAYER2 = 2
NUMFORWIN = 4

class match:
    board = []
    nameP1 = ''
    nameP2 = ''
    charP1 = ''
    charP2 = ''
    scores = [0, 0]
    HEIGHT = 6; WIDTH =7
    emptySpaces = HEIGHT * WIDTH

    def __init__(self, nameP1, nameP2, charP1, charP2, scores):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], ]
        self.nameP1 = nameP1
        self.nameP2 = nameP2
        self.charP1 = charP1
        self.charP2 = charP2
        self.scores = scores


def showBoard(match:match):
    print("")
    print(colored(f"Player 1 - {match.scores[PLAYER1]}", "red"), end="")
    print(colored(f" | Player 2 - {match.scores[PLAYER2]} ", "blue"), end="")
    print(f"Turn - {match.scores[0]}")
    for i in range(0, match.HEIGHT):
        for j in range(0, match.WIDTH):
            if match.board[i][j] == 0:
                print(colored("| |", "white"), end="")
            elif match.board[i][j] == 1:
                print(colored(f"|{match.charP1}|", "red"), end="")
            else:
                print(colored(f"|{match.charP2}|", "blue"),end="")
        print("")
    for i in range(0, match.WIDTH):
        print(colored(f"|{i+1}|", "white"), end="")
    print("")
    
def playerInput(player: int, match:match):
    retry = True
    col = -1
    if player == 1:
        char = match.charP1
    else:
        char = match.charP2
    while retry:
        try:
            col = int(input(f"Player {player} place a piece({char}): ")) -1
            while col<0 or col>match.WIDTH:
                print(f"Choose a number between 1 and {match.WIDTH}")
                col = int(input(f"Player {player} place a piece({char}): ")) -1
            return col 
        except ValueError:
            print("Please enter a number")

def addPiece(player: int, col: int, match:match):
    # add piece to free row and return the number of the row
    retry = True
    while retry:
        if match.board[0][col] != 0:
            print("Cant place there")
            col = playerInput(player, match)
        else:
            retry = False
            for i in range(0, match.HEIGHT):
                if match.board[5-i][col] == 0:
                    match.board[5-i][col] = player
                    return 5-i
            
def checkVertical(player: int, row: int, col: int, match:match):
    # teste Vertical se conectado 4 a partir da ultima peca adicionada
    test = True
    tempCol = col; tempRow = row
    connected = 1
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica se as proximas 3 pecas abaixo da ultima adicionada pertence ao mesmo player
        if tempRow + 1 <= match.HEIGHT -1:
            tempRow += 1
            if match.board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        else:
            return False

def checkHorizontal(player: int, row: int, col: int, match:match):
    # teste Horizontal se conectado 4 a partir da ultima peca adicionada
    test = True; left = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas a esquerda da ultima adicionada pertencem ao mesmo player 
        if left:
            if tempCol - 1 >= 0:
                tempCol -= 1
                if match.board[tempRow][tempCol] == player:
                    connected += 1
                else:
                    tempCol = col
                    left = False
            else:
                tempCol = col
                left = False
        # se nao tiver mais pecas a esquerda volta a posicao da ultima adicionada e verifica as pecass a direita
        elif tempCol + 1 <= match.WIDTH -1:
            tempCol += 1
            if match.board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        else: 
            return False

def checkDiag1(player: int, row: int, col: int, match:match):
    # teste diagonal / se conectado 4 a partir da ultima peca colocada
    test = True; bottomLeft = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas na diagona(/) esquerda perntencem ao player
        if bottomLeft:
            if tempCol - 1 >= 0 and tempRow + 1 <= match.HEIGHT -1:
                tempCol -= 1; tempRow += 1
                if match.board[tempRow][tempCol] == player:
                    connected += 1
                else:
                    tempCol = col; tempRow = row
                    bottomLeft = False
            else:
                tempCol = col; tempRow = row
                bottomLeft = False
        # se nao tiver mais pecas na diagonal(/) esqueda verifica as da diagonal(/) direita  
        elif tempCol + 1 <= match.WIDTH -1 and tempRow - 1 >= 0:
            tempCol += 1; tempRow -= 1
            if match.board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False 
        else:
            return False
        
def checkDiag2(player: int, row: int, col: int, match:match):
    # teste diagonal \ se conectado 4 a partir da ultima peca colocada
    test = True; uppperLeft = True
    tempCol = col; tempRow = row
    connected = 1   
    while test:
        if connected == NUMFORWIN:
            return True
        # verifica quantas pecas na diagona(\) esquerda perntencem ao player
        if uppperLeft:
            if tempCol - 1 >= 0 and tempRow - 1 >= 0:
                tempCol -= 1; tempRow -= 1
                if match.board[tempRow][tempCol] == player:
                    connected += 1  
                else:
                    tempCol = col; tempRow = row
                    uppperLeft = False
            elif uppperLeft:
                tempCol = col; tempRow = row
                uppperLeft = False
        # se nao tiver mais pecas na diagonal(\) esqueda verifica as da diagonal(\) direita 
        elif tempCol + 1 <= match.WIDTH -1 and tempRow + 1 <= match.HEIGHT -1:
            tempCol += 1; tempRow += 1
            if match.board[tempRow][tempCol] == player:
                connected += 1
            else:
                return False
        else:
            return False

def checkWin(player: int, row: int, col: int, match:match):
    # verifica se o player ganhou ou se ocorreu um empate
    global empitySpaces
    if empitySpaces <= 0:
        return -1
    else:
        empitySpaces -= 1
        if checkVertical(player, row, col, match) or checkHorizontal(player, row, col, match) or checkDiag1(player, row, col, match) or checkDiag2(player, row, col, match):
            if player == PLAYER1:
                return 1
            elif player == PLAYER2:
                return 2

def gameStarter():
    if rd.random() <= 0.5:
        return 1
    else:
        return 2
'''
# os scores dos player em que i=0 turno, i=1 player 1, i=2 player 2
scores = [0,0,0]
#while loop se continua com jogos novos
while not QUIT: 
    scores[0] = 0
    # game board 
    board = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],]

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
    turn = gameStarter()
    if turn==1:
        turnP1 = True
        print("Player 1 Starts")
    else:
        turnP1 = False
        print("Player 2 Starts")

    showBoard()
    # while loop do jogo que esta ocorrendo
    while GAME:
        scores[0] += 1
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
            scores[PLAYER1] += 1
            GAME = False
        elif result == -1:
            print("Draw")
            scores[PLAYER2] += 1
            GAME = False
    valid = True
    while valid:
        replay= input("Replay?(y/n): ").lower()
        if replay == "n":
            valid = False
            QUIT = True
        elif replay == "y":
            valid = False
            GAME = True         
'''