import socket
from sys import argv

if len(argv) != 3:
    print('Invalid arguments. Please specify SERVER_ADDRESS and SERVER_PORT')
    exit(-1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)
    try:
        s.connect((argv[1], int(argv[2])))
    except:
        print("Couldn't connect to the server.")
        exit(1)
    print("Connected.")
    try:
        while(True):
            data = s.recv(1024)
            if not data:
                print("Connection closed.")
                break
            print(data.decode("UTF-8"))
            message = input("> ")
            s.send(message.encode())
    except Exception as e:
        print("Something went wrong, connection closed.")
        print(e)
