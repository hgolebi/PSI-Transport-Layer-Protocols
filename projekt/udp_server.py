import socket

ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8123

with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
    s.bind((ADDRESS, PORT))
    print("UDP server up and listening on ", ADDRESS, PORT)
    while(True):
        # device registration
        data, device = s.recvfrom(2)
        if not data:
            print("Device hasn't send any data")
            continue
        id = int.from_bytes(data, "big")
        ret = s.sendto(data, device)
        if ret != len(data):
            print("Error while sending response")
            continue

        while(True):
            # client message imitation
            cfg = input('cfg: ')
            print(int(cfg, base=2))
            cfg_byte = int(cfg, base=2).to_bytes(1, 'big')
            val = input('val: ')
            val_bytes = int(val).to_bytes(2, 'big')

            # communication with device
            print(cfg_byte + val_bytes)
            ret = s.sendto(cfg_byte + val_bytes, device)
            if ret != 3:
                print("Error while sending message")
                exit(-1)
            data, device = s.recvfrom(2)
            if not data:
                print("Error while receiving response")
                exit(-1)
            print('DEVICE: ', int.from_bytes(data, 'big'))


