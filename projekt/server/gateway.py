"""
Brama komunikacyjna dla urządzeń sensorycznych
Hubert Gołębiowski, Bartosz Pomiankiewicz, Bartłomiej Rodzik
20.05.2023
"""
import socket
from sys import argv
import threading
import select

from command_interpreter import analyze_message, HELP_MESSAGE, EXIT_CODE
from logger import Logger
from udp_server import DeviceManager
from codes_and_messages import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
UDP_PORT = 8001

def client_service_thread(conn, addr):
    with conn:
        conn.setblocking(False)
        try:
            select.select([], [conn], [], 5)
            conn.send(START_MESSAGE.encode('UTF-8'))
        except Exception as e:
            logger.error(SEND_ERROR, CONN_CLOSED_MESSAGE)
            logger.error(e)
            return
        while True:
            try:
                rl, _, _ = select.select([conn], [], [], 5)
                if not rl:
                    continue
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('UTF-8')
                logger.log(f"Client {addr}: {message}")
                reply = analyze_message(message)
                if reply == EXIT_CODE:
                    conn.shutdown(socket.SHUT_RDWR)
                    break
                select.select([], [conn], [], 5)
                conn.send(str(reply).encode('UTF-8'))
            except Exception as e:
                logger.error(CONNECTION_ERROR)
                logger.error(e)
                break
        conn.close()
    logger.log(f"Connection closed. {addr}")


if len(argv) > 1 and argv[1].isdigit() and int(argv[1]) > 0:
    buffer_size = int(argv[1])

logger = Logger()

# Initialize UDP server in another thread
threading.Thread(None, DeviceManager.start, 'udp_server_thread', (HOST, UDP_PORT, logger), daemon=True).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.setblocking(False)
    s.listen(10)
    logger.log(f"Started listening on {HOST} {PORT}")
    while True:
        try:
            rl, _, _ = select.select([s], [], [], 5)
            if not rl:
                continue
            conn, addr = s.accept()
            logger.log(f"Connected by {addr}")
            threading.Thread(target=client_service_thread, args=[conn, addr, ], daemon=True).start()
        except Exception as e:
            logger.error(e)
            continue
