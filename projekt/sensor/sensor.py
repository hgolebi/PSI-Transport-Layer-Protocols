"""
Brama komunikacyjna dla urządzeń sensorycznych
Hubert Gołębiowski, Bartosz Pomiankiewicz, Bartłomiej Rodzik
27.05.2023
"""
import socket
from sys import argv
import random
from select import select
import ipaddress

SENSOR_ID = random.randrange(0, 2**16-1)
REGISTERS = [10 * n for n in range(8)]
ADDRESS = socket.gethostbyname(socket.gethostname())


if len(argv) != 3:
    print('Invalid arguments. Please specify SERVER_ADDRESS and SERVER_PORT')
    exit(-1)

# try:
#     ipaddress.ip_address(argv[1])
# except ValueError:
#     print("Invalid argument. SERVER_ADDRESS must be ip address")
#     exit(-1)
try:
    int(argv[2])
except:
    print("Invalid argument. SERVER_PORT must be integer")
    exit(-1)

server = (argv[1], int(argv[2]))

print("Sensor ID: ", SENSOR_ID)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setblocking(False)
    s.bind((ADDRESS, 0))
    id_bytes = SENSOR_ID.to_bytes(2, 'big')
    select([], [s], [], 5)
    try:
        n = s.sendto(id_bytes, server)
        if n != 2:
            print("Error while sending initial message")
            exit(-1)
    except Exception as e:
           print(f"Error: {e}")
           exit(-1)     
    rl, _, _ = select([s], [], [], 5)
    return_data, _ = s.recvfrom(2)
    if return_data != id_bytes:
        print('Error while connecting to the server')
        exit(-1)
    while True:
        rl, _, _ = select([s], [], [], 5)
        if not rl:
            continue
        data, device_manager = s.recvfrom(3)
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
        else:
            val = int.from_bytes(data[1:3], 'big')
            REGISTERS[id] = val
        select([], [s], [], 5)
        s.sendto(val.to_bytes(2, 'big'), device_manager)  # sensor sends back the value to confirm success
