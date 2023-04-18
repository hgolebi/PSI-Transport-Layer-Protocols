import socket
from sys import argv

# HOST = "127.0.0.1" 
HOST = socket.gethostname()
PORT = 8000  
RESPONSE = b"Odpowiedz serwera"

buffer_size = 1024
if len(argv) > 1 and argv[1].isdigit() and int(argv[1]) > 0:
    buffer_size = int(argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(5)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Started listening on {HOST}:{PORT}")
    while True:
        try:
            conn, addr = s.accept()
        except TimeoutError:
            print("No connections. Timing out.")
            exit()
        with conn:
            conn.settimeout(10)
            print(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(buffer_size)
                    if not data:
                        break
                    print(f"Client : {data.decode('UTF-8')}")
                    conn.send(RESPONSE)
                except:
                    continue
        print("Connection closed")