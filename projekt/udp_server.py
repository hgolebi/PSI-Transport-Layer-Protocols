import socket
import threading
from time import sleep

ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8123

class DeviceManager:
    devices = {}
    
    @classmethod
    def start(cls, address, port, logger):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            s.bind((address, port))
            # print("UDP server up and listening on ", address, port)
            cls.logger = logger
            cls.logger.log(f"UDP server up and listening on {address} {port}")
            threading.Thread(target=DeviceManager.check_devices, daemon=True).start()
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
                cls.logger.log(f"Device {id=} added to connected list")


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

    @classmethod
    def check_devices(cls):
        while True:
            for id, dev in list(cls.devices.items()):
                with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
                    try:
                        s.settimeout(5)
                        # communication with device
                        ret = s.sendto(int(0).to_bytes(3, 'big'), dev)
                        if ret != 3:
                            cls.logger.log(f"Error while pinging device {id=} (sending)")
                            # print("Error while sending message")
                            cls.devices.pop(id)
                            cls.logger.log(f"Removed device {id=} from active list")
                            break

                        data, _ = s.recvfrom(2)
                        if not data:
                            cls.logger.log(f"Error while pinging device {id=} (receiving)")
                            cls.devices.pop(id)
                            cls.logger.log(f"Removed device {id=} from active list")
                            break
                            # print("Error while receiving response")
                    except TimeoutError:
                        cls.logger.log(f"Error while pinging device {id=} (timeout)")
                        # print("Error while sending message")
                        cls.devices.pop(id)
                        cls.logger.log(f"Removed device {id=} from active list")
                    except Exception as e:
                        cls.logger.log(f"Error while pinging device {id=} ({e})")
                        cls.devices.pop(id)
                        cls.logger.log(f"Removed device {id=} from active list")


            sleep(10)
