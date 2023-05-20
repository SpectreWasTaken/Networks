import socket


def getRequest():
    """Gets the First Packet and unpacks it

    Args:
        bytesAddressPair (Array): Has File Info and IP stored as 'Type:<typing> Name:<filename>"
    """
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = ""
    temp = bytesAddressPair[0]
    for letter in temp:
        message = message + letter
    message = message.split(' ')
    type = None
    i = 0
    for info in message:
        info = info.decode('utf-8')
        type[i] = info.split(':')[1]
        i=i+1
    return type


localIP = 'localhost'
localPort = 3030
bufferSize = 1024

msgFromServer = 'Hello UDP Client!'
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(
    family=socket.AF_INET,
    type= socket.SOCK_DGRAM
)

UDPServerSocket.bind((localIP, localPort))

print('UDP Server up and listening! Port:3030')

print(getRequest())

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(bytesAddressPair)
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    UDPServerSocket.sendto(bytesToSend, address)
    
