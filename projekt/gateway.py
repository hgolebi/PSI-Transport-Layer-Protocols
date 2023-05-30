import socket
from sys import argv
from command_interpreter import analyze_message, HELP_MESSAGE, EXIT_CODE
from logger import Logger
from udp_server import DeviceManager

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000

START_MESSAGE = "Connected to the gateway." + HELP_MESSAGE
CONN_CLOSED_MESSAGE = "Connection closed."
# ERROR messages
SEND_ERROR = "ERROR: Couldn't send the message."

buffer_size = 1024
if len(argv) > 1 and argv[1].isdigit() and int(argv[1]) > 0:
    buffer_size = int(argv[1])

logger = Logger()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    logger.log(f"Started listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            logger.log(f"Connected by {addr}")
            try:
                conn.send(START_MESSAGE.encode('UTF-8'))
            except Exception as e:
                logger.log(SEND_ERROR, CONN_CLOSED_MESSAGE)
                logger.log(e)
                break
            while True:
                try:
                    data = conn.recv(buffer_size)
                    if not data:
                        break
                    message = data.decode('UTF-8')
                    logger.log(f"Client: {message}")
                    reply = analyze_message(message)
                    if reply == EXIT_CODE:
                        conn.shutdown(socket.SHUT_RDWR)
                        break
                    conn.send(reply.encode('UTF-8'))
                except Exception as e:
                    logger.log(e)
                    break
            conn.close()
        logger.log("Connection closed.")
        logger.log(f"Listening on {HOST}:{PORT}")