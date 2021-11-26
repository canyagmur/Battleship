from socket import *


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))
serverSocket.listen(1)


print("The server is ready to receive")
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        sentence_from_client = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence_from_client.upper()
        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()
    except KeyboardInterrupt:
        print("Bye")
        break