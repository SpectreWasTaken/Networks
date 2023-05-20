import socket

msgFromClient = "Type:PDF Name:Example"
bytesToSend = msgFromClient.encode('utf-8')
serverAddressPort = ("localhost", 3030)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer, serverAddress = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server: {}".format(msgFromServer.decode('utf-8'))
print(msg)
