import socket
from sys import argv

# HOST = "127.0.0.1" 
HOST = socket.gethostname()
PORT = 8000  


HELP_MESSAGE = '''
Available commands:
> help                              - shows available commands.
> ping SENSOR_ID                    - checks if sensor is available.
> read SENSOR_ID REGISTER           - reads value in the given register.
> config SENSOR_ID REGISTER VALUE   - sets register to the given value.
> exit                              - closes connection.
'''
START_MESSAGE = "Connected to the gateway.\n\n" + HELP_MESSAGE
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
    print(f"Started listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            try:
                conn.send(START_MESSAGE.encode('UTF-8'))
            except Exception as e:
                print(e)
                print(SEND_ERROR, CONN_CLOSED_MESSAGE)
                continue
            while True:
                data = conn.recv(buffer_size)
                client_message = data.decode('UTF-8')
                if not data:
                    break
                print(f"Client : {client_message}")
                try:
                    conn.send(b"Received message.")
                except:
                    print(SEND_ERROR, CONN_CLOSED_MESSAGE)
                    continue
        print("Connection closed.")