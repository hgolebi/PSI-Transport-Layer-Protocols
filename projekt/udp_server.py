import socket

ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8123

class DeviceManager:
    devices = {}
    
    @classmethod
    def start(cls, address, port):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            s.bind((address, port))
            print("UDP server up and listening on ", address, port)
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
                cls.devices[id] = device

    @classmethod
    def read_from_device(cls, device_id, register):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            zero = 0
            register = register & 7
            query_byte = register.to_bytes(1, 'big')
            value_bytes = zero.to_bytes(2, 'big') 
            ret = s.sendto(query_byte + value_bytes, cls.devices[device_id])
            if ret != 3:
                print("Error while sending message")
                return -1       # TO DO
            data, _ = s.recvfrom(2)
            if not data:
                print("Error while receiving response")
                return -2       # TO DO
            return int.from_bytes(data, 'big')

    @classmethod
    def config_device(cls, device_id, register, value):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            register = register | 8
            query_byte = register.to_bytes(1, 'big')
            value_byte = value.to_bytes(2, 'big')
            # communication with device
            ret = s.sendto(query_byte  + value_byte, cls.devices[device_id])
            if ret != 3:
                print("Error while sending message")
                return -1       # TO DO
            data, _ = s.recvfrom(2)
            if not data:
                print("Error while receiving response")
                return -2       # TO DO
            if data != value_byte:
                print("Device returned different configuration")
                return -3       # TO DO
            return int.from_bytes(data, 'big')

    @classmethod
    def list_devices(cls):
        return(cls.devices)