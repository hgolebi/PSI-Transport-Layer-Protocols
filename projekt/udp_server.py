import socket
import threading
from time import sleep
from select import select
from codes_and_messages import *

ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8123

class DeviceManager:
    devices = {}

    @classmethod
    def start(cls, address, port, logger):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            s.bind((address, port))
            s.setblocking(False)
            # print("UDP server up and listening on ", address, port)
            cls.logger = logger
            cls.logger.log(f"UDP server up and listening on {address} {port}")
            threading.Thread(target=DeviceManager.check_devices, daemon=True).start()
            while(True):
                # device registration
                rl, _, _ = select([s], [], [], 5)
                if not rl:
                    continue
                data, device = s.recvfrom(2)
                if not data:
                    print("Device hasn't send any data")
                    continue
                id = int.from_bytes(data, "big")
                select([], [s], [], 5)
                ret = s.sendto(data, device)
                if ret != len(data):
                    print("Error while sending response")
                    continue
                cls.devices[id] = device
                cls.logger.log(f"Device {id=} added to connected list")


    @classmethod
    def read_from_device(cls, device_id, register):
        if not cls.ping(device_id):
            return DEVICE_NOT_ACTIVE_CODE
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            s.setblocking(False)
            register = register & 7
            query_byte = register.to_bytes(1, 'big')
            value_bytes = int(0).to_bytes(2, 'big')
            select([], [s], [], 5)
            ret = s.sendto(query_byte + value_bytes, cls.devices[device_id])
            if ret != 3:
                print("Error while sending message")
                return MESSAGE_SENT_INCORRECTLY_CODE       # TO DO
            select([s], [], [], 5)
            data, _ = s.recvfrom(2)
            if not data:
                print("Error while receiving response")
                return DID_NOT_RECEIVE_DATA_CODE       # TO DO
            return int.from_bytes(data, 'big')

    @classmethod
    def config_device(cls, device_id, register, value):
        if not cls.ping(device_id):
            return DEVICE_NOT_ACTIVE_CODE
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            s.setblocking(False)
            register = register | 8
            query_byte = register.to_bytes(1, 'big')
            value_byte = value.to_bytes(2, 'big')
            # communication with device
            select([], [s], [], 5)
            ret = s.sendto(query_byte  + value_byte, cls.devices[device_id])
            if ret != 3:
                print("Error while sending message")
                return MESSAGE_SENT_INCORRECTLY_CODE       # TO DO
            select([s], [], [], 5)
            data, _ = s.recvfrom(2)
            if not data:
                print("Error while receiving response")
                return DID_NOT_RECEIVE_DATA_CODE       # TO DO
            if data != value_byte:
                print("Device returned different configuration")
                return VALUES_DOES_NOT_EQUAL_CODE       # TO DO
            return int.from_bytes(data, 'big')

    @classmethod
    def list_devices(cls):
        return(cls.devices)

    @classmethod
    def ping(cls, id):
        device = cls.devices[id]
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
            try:
                s.settimeout(5)
                # communication with device
                ret = s.sendto(int(0).to_bytes(3, 'big'), device)
                if ret != 3:
                    cls.logger.error(f"Pinging device {id=} (sending)")
                    # print("Error while sending message")
                    cls.devices.pop(id)
                    cls.logger.log(f"Removed device {id=} from active list")
                    return False

                data, _ = s.recvfrom(2)
                if not data:
                    cls.logger.error(f"Pinging device {id=} (receiving)")
                    cls.devices.pop(id)
                    cls.logger.log(f"Removed device {id=} from active list")
                    return False
                    # print("Error while receiving response")
            except TimeoutError:
                cls.logger.error(f"Pinging device {id=} (timeout)")
                # print("Error while sending message")
                cls.devices.pop(id)
                cls.logger.log(f"Removed device {id=} from active list")
                return False
            except Exception as e:
                cls.logger.error(f"Pinging device {id=} ({e})")
                cls.devices.pop(id)
                cls.logger.log(f"Removed device {id=} from active list")
                return False
        return True

    @classmethod
    def check_devices(cls):
        while True:
            # try:
            for id in list(cls.devices):
                cls.ping(id)
            sleep(10)
            # except:
            #     continue
