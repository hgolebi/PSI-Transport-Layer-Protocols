import socket
from sys import argv


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((argv[1], int(argv[2])))
    except:
        print("Couldn't connect to the server.")
        exit(1)
    print("Connected.")
    s.send(b"aaaaaBBBBBcccccDDDDDeeeeeFF")
    print("Message sent.")
    data = s.recv(1024)

print(f"Received response: {data.decode('UTF-8')}")