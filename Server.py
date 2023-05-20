import socket
from API import *

def getRequest():
    """Gets the First Packet and unpacks it

    Returns:
        dict: Contains file type and name
    """
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    
    message = bytesAddressPair[0].decode('utf-8')
    info = message.split(' ')
    file_info = {}
    for i in info:
        data = i.split(':')
        file_info[data[0]] = data[1]
    UDPServerSocket.sendto('200 OK'.encode('utf-8'), bytesAddressPair[1])
    return file_info

localIP = 'localhost'
localPort = 3030
bufferSize = 1024

msgFromServer = 'Hello UDP Client!'
bytesToSend = msgFromServer.encode('utf-8')

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print('UDP Server up and listening! Port: 3030')

file_info = getRequest()
print(file_info)

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client: {}".format(message.decode('utf-8'))
    clientIP = "Client IP Address: {}".format(address)
    print(clientMsg)
    print(clientIP)
    UDPServerSocket.sendto(bytesToSend, address)
