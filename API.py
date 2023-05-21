import socket
import os


def getRequest(bytesAddressPair, UDPServerSocket, Connections, bufferSize=1024):
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
        UDPServerSocket.sendto('404 NOT FOUND'.encode(
            'utf-8'), bytesAddressPair[1])


def startHandshake(bytesAddressPair, UDPServerSocket, Connections, bufferSize=1024):
    """Starts the Handshake Connectivity between the Client and Server

    Args:
        UDPServerSocket (Connection): The Connection Used to get and recieve data
        bufferSize (int, optional): The Buffer Size Used. Defaults to 1024.
        Connections(list): The List of IPs Connected to

    Returns:
        list: After Appending the new IP
    """
    if inConnections(bytesAddressPair[1], Connections) == False:
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


def getFiles(dir='dir'):
    """Get All files in storage directory

    Args:
        dir (str): Selects a directory to read from. Defaults to 'dir'.

    Returns:
        list: all files in a folder
    """
    return os.scandir(dir).apply(lambda x: x.split('.'))


def reqHandshake(serverIP):
    """starts the Handshake connectivity

    Args:
        serverIP (tuple): the IP the server is based in

    Returns:
        Connection: Connection needed to communicate
    """
    UDPClientSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto('HANDSHAKE'.encode('utf-8'), serverIP)
    return UDPClientSocket


def connectionType(bytesAddressPair, UDPServerSocket, Connections):

    if bytesAddressPair[0].decode['utf-8'] == 'HANDSHAKE':
        return startHandshake(bytesAddressPair, UDPServerSocket, Connections)
    elif (bytesAddressPair[0].decode['utf-8'][:3] == "GET") and (bytesAddressPair[1] in Connections):
        return sendFile(UDPServerSocket, Connections, bytesAddressPair[0].decode('utf-8')[3:len(bytesAddressPair[0].decode('utf-8'))], bytesAddressPair[0].decode('utf-8')[3-len(bytesAddressPair[0].decode('utf-8')):len(bytesAddressPair[0].decode('utf-8'))], bytesAddressPair[1])


def sendFile(UDPServerSocket, Connections, fileName, filetype, clientIp):
    if filetype != 'txt':
        UDPServerSocket.sendto("404 NOT FOUND".encode('utf-8'), clientIp)
    elif fileName not in getFiles():
        UDPServerSocket.sendto("404 NOT FOUND".encode('utf-8'), clientIp)
    else:
        f = open((fileName+"." + filetype), 'rb')
        data = f.read(1024)
        UDPServerSocket.sendto(fileName, clientIp)
        UDPServerSocket.sendto(data, clientIp)
        while (data):
            if (UDPServerSocket.sendto(data, clientIp)):
                print("Sent Packet... Waiting For Confirmation...")
                if (UDPServerSocket.recvfrom(1024)[0].decode('utf-8') == "200 OK"):
                    data = f.read(1024)
                else:
                    continue
        UDPServerSocket.sendto('FILE SENT'.encode('utf-8'), clientIp)


def recFile(UDPServerSocket, FileName, Server):
    UDPServerSocket.sendto(FileName, Server)
    data, addr = UDPServerSocket.recvfrom(1024)
    print('Recieved File:', data.strip())
    f = open(data.strip(), 'wb')

    data, addr = UDPServerSocket.recvfrom(1024)
    while (data):
        try:
            if data == "FILE SENT":
                f.close
                break
            f.write(data)
            UDPServerSocket.settimeout(2)
            UDPServerSocket.sendto('200 OK'.encode('utf-8'), Server)
            data, addr = UDPServerSocket.recvfrom(1024)
        except timeout:
            UDPServerSocket.sendto('FAILED'.encode('utf-8'))
