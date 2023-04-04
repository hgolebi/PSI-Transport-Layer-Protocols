import socket
import sys

msgFromClient = "Hello from client"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 8080)
bufferSize = 1024

serverAddressPort = (sys.argv[1], int(sys.argv[2]))

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

for i in range(3):
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Server : {}".format(str(msgFromServer[0]))

    print(msg)
