# THIS SERVER ONLY ACCEPTS ONE CLIENT
# THE MESSAGES ARE EXCHANGED ONLY BETWEEN SERVER AND CLIENT

import socket

def serverProgram():
    # get hostname
    host=socket.gethostname()
    port = 5000 # acho que dá pra deixar pro usuário escolher depois, mas por hora é isso aqui mesmo
                # não iniciar com qualquer port abaixo de 1024 (são reservadas)

    serverSocket = socket.socket() #get instance
    serverSocket.bind((host, port))

    # configure how many clients can listen simultaneously (2)
    serverSocket.listen(4)
    conn, address = serverSocket.accept() # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream, won´t accept anything bigger than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode()) # send data to cliente

    conn.close() # close the connection

if __name__ == '__main__':
    serverProgram()
