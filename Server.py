import socket


def getRequest():
    """Gets the First Packet and unpacks it

    Args:
        bytesAddressPair (Array): Has File Info and IP stored as 'Type:<typing> Name:<filename>"
    """
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    print(bytesAddressPair)
    UDPServerSocket.sendto(b'recieved', bytesAddressPair[1])

    
    message = bytesAddressPair[0].decode('utf-8')
    # for letter in temp:
    #     message = message + str(letter)
    # message = message.split(' ')
    i = 0
    for info in message:
        info = info
        print(info)
        type[i] = info.split(':')[1]
        i=i+1    
    UDPServerSocket.sendto(bytesToSend, address)
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
    
