import socket


localIP = "127.0.0.1"
localPort = 8080
bufferSize = 1024

msgFromServer = "Reply from server"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((socket.gethostname(), localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Client ({}) : {}".format(address, message)
    
    print(clientMsg)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
