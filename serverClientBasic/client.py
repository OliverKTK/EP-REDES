# THIS CLIENT STRUTURE ONLY WORKS FOR ONE CLIENT

import socket

def clienteProgram():
    host = socket.gethostname() # as both codes are running on the same PC (needs to fix for multiple machines)
    port = 5000 # socket server port number (needs to fic for multiple machines)

    clientSocket = socket.socket() # instanciate
    clientSocket.connect((host, port)) # connect to server

    message = input(' -> ')

    while message.lower().strip() != 'bye': # exit code
        # the way it is implemented means that a user must receive an answer before being
        # able to send another message
        clientSocket.send(message.encode()) # send message
        data = clientSocket.recv(1024).decode() # receive response

        print('Received from server: ' + data) # show in terminal

        message = input(' -> ') # take new input

    clientSocket.close() # close the connection

if __name__ == '__main__':
    clienteProgram()