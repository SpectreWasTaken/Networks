import socket
def getRequest(UDPServerSocket, Connections,bufferSize = 1024):
    """Waits for the Request for the file info

    Args:
        UDPServerSocket (Connection): The Connection Used to get and recieve data
        bufferSize (int, optional): The Buffer Size Used. Defaults to 1024.

    Returns:
        file_info: all the Info of the File tokenized
    """
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    if inConnections(bytesAddressPair[1], Connections):    
        message = bytesAddressPair[0].decode('utf-8')
        info = message.split(' ')
        file_info = {}
        for i in info:
            data = i.split(':')
            file_info[data[0]] = data[1]
        UDPServerSocket.sendto('200 OK'.encode('utf-8'), bytesAddressPair[1])
        return file_info
    else:
        UDPServerSocket.sendto('404 NOT FOUND'.encode('utf-8'), bytesAddressPair[1])


def startHandshake(UDPServerSocket, Connections, bufferSize = 1024):
    """Starts the Handshake Connectivity between the Client and Server

    Args:
        UDPServerSocket (Connection): The Connection Used to get and recieve data
        bufferSize (int, optional): The Buffer Size Used. Defaults to 1024.
        Connections(list): The List of IPs Connected to
        
    Returns:
        list: After Appending the new IP
    """
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    if inConnections(bytesAddressPair[1], Connections):
        Connections.append(bytesAddressPair[1])
    UDPServerSocket.sendto('200 OK'.encode('utf-8'), bytesAddressPair[1])
    return Connections

def inConnections(IP, Connections):
    """Check if IP in Connections

    Args:
        IP (IP): The IP value to Test
        Connections (list): list of established connections

    Returns:
        boolean: if ip in connections, return true
    """
    return IP in Connections
