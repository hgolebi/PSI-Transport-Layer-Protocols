import socket
from sys import argv
import random

SENSOR_ID = random.randrange(0, 2**16-1)
REGISTERS = [10 * n for n in range(8)]
ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 10123

if len(argv) != 3:
    print('Invalid arguments. Please specify SERVER_ADDRESS and SERVER_PORT')
    exit(-1)
server = (argv[1], int(argv[2]))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    id_bytes = SENSOR_ID.to_bytes(2, 'big')
    n = s.sendto(id_bytes, server)
    if n != 2:
        print("Error while sending initial message")
        exit(-1)
    return_data, _ = s.recvfrom(2)
    if return_data != id_bytes:
        print('Error while connecting to the server')
        exit(-1)
    while True:
        data, _ = s.recvfrom(3)
        if not data:
            print("no data")
            continue

        # | - - - - rw id id id | h h h h h h h h | l l l l l l l l |
        # fist 4 bits are not interpreted
        # 5th bit: 0 - read from register, 1 - write to register
        # 6th, 7th and 8th bit: register id (6th bit is msb, 8th bit is lsb)
        # 2nd byte represents most significant byte of the value
        # 3rd byte represents least significant byte of the value
        print(data)
        write = (data[0] >> 3) & 1
        id = data[0] & 7
        if (not write):
            val = REGISTERS[id]
            s.sendto(val.to_bytes(2, 'big'), server)
        else:
            val = int.from_bytes(data[1:3], 'big')
            REGISTERS[id] = val
            s.sendto(val.to_bytes(2, 'big'), server)  # sensor sends back the value to confirm success
