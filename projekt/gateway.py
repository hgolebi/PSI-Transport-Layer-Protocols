import socket
from sys import argv
from command_parser import analyze_message, HELP_MESSAGE, EXIT_CODE

# HOST = "127.0.0.1"
HOST = socket.gethostname()
PORT = 8000



START_MESSAGE = "Connected to the gateway.\n" + HELP_MESSAGE
CONN_CLOSED_MESSAGE = "Connection closed.\n"
# ERROR messages
SEND_ERROR = "ERROR: Couldn't send the message.\n"

buffer_size = 1024
if len(argv) > 1 and argv[1].isdigit() and int(argv[1]) > 0:
    buffer_size = int(argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Started listening on {HOST}:{PORT}\n")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            try:
                conn.send(START_MESSAGE.encode('UTF-8'))
            except Exception as e:
                print(SEND_ERROR, CONN_CLOSED_MESSAGE)
                print(e)
                break
            while True:
                try:
                    data = conn.recv(buffer_size)
                    if not data:
                        break
                    message = data.decode('UTF-8')
                    print(f"Client: {message}")
                    reply = analyze_message(message)
                    if reply == EXIT_CODE:
                        conn.shutdown(socket.SHUT_RDWR)
                        break
                    conn.send(reply.encode('UTF-8'))
                except Exception as e:
                    print(e)
                    break
            conn.close()
        print("Connection closed.")
        print(f"Listening on {HOST}:{PORT}\n")