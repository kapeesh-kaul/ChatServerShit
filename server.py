import socket
import select

HEADERSIZE = 10
ip = '127.0.0.1'
port = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((ip, port))
serverSocket.listen()

socketsList = [serverSocket]
clients = {}

def receiveMessage(clientSocket):
        try:
            messageHeader = clientSocket.recv(HEADERSIZE)
            if not len(messageHeader):
                return False
            messageLength = int(messageHeader.decode('utf-8').strip())
            return {'header':messageHeader, 'data':clientSocket.recv(messageLength)}
        except:
            return False


while True:
    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)
    for notifiedSocket in readSockets:
            if notifiedSocket == serverSocket:
                clientSocket, clientAddress == serverSocket.accept()
                user = receiveMessage(clientSocket)
                if user is False:
                    continue
                socketsList.append(clientSocket)
                clients[clientSocket] = user
                print(f"accepeted a new connection form {clientAddress[0]:clientAddress[1]} username: {user['data'].decode('utf-8')}")
            else:
                message = receiveMessage(notifiedSocket)
                if message is False:
                    print(f"Cloed connection form {clients[notifiedSocket]['data'].decode('utf-8')}")
                    socketsList.remove(notifiedSocket)
                    del clients[notifiedSocket]
                    continue
                user = clients[notifiedSocket]
                print(f"Rcvd msg from {user[data].decode('utf-8')}: {message['data'].decode('utf-8')}")

                for clientSocket in clients:
                    if clientSocket != notifiedSocket:
                        clientSocket.send(user['header']+user['data']+message['header']+message['data'])
    for notifiedSocket in exceptionSockets:
        socketsList.remove(notifiedSocket)
        del clients[notifiedSocket]
