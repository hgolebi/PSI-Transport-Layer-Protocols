from udp_server import DeviceManager
from tabulate import tabulate
from codes_and_messages import *

def ping_command(message_list):
    pass


def read_command(message_list):
    if len(message_list) != 3:
        return 'Wrong number of arguments.\nUsage: read SENSOR_ID REGISTER'
    command, device_id, register = message_list
    device_id = device_id_check(device_id)
    if device_id is None:
        return WRONG_DEVICE_ID_MESSAGE
    if device_id == DEVICE_NOT_ACTIVE_CODE:
        return DEVICE_NOT_ACTIVE_MESSAGE
    register = register_check(register)
    if register is None:
        return WRONG_REGISTER_MESSAGE

    return DeviceManager.read_from_device(device_id, register)
    # return f'{command} {str(device_id)} {str(register)}'



def config_command(message_list):
    # argument number check
    if len(message_list) != 4:
        return 'Wrong number of arguments.\nUsage: config SENSOR_ID REGISTER VALUE'
    command, device_id, register, value = message_list
    device_id = device_id_check(device_id)
    if device_id is None:
        return WRONG_DEVICE_ID_MESSAGE
    if device_id == DEVICE_NOT_ACTIVE_CODE:
        return DEVICE_NOT_ACTIVE_MESSAGE
    register = register_check(register)
    if register is None:
        return WRONG_REGISTER_MESSAGE
    value = value_check(value)
    if value is None:
        return WRONG_VALUE_MESSAGE

    return DeviceManager.config_device(device_id, register, value)
    # return f'{command} {str(device_id)} {str(register)} {str(value)}'


def device_id_check(device_id):
    try:
        device_id = int(device_id)
    except:
        return None
    if device_id < 0:
        return None
    device_list = DeviceManager.list_devices()
    if device_id not in device_list:
        return DEVICE_NOT_ACTIVE_CODE
    return device_id

def register_check(register):
    if len(register) < 3:
        try:
            register = int(register)
        except:
            return None
    elif register[:2] == '0b':
        try:
            register = int(register, 2)
        except:
            return None
    elif register[:2] == '0x':
        try:
            register = int(register, 16)
        except:
            return None
    else:
        try:
            register = int(register)
        except:
            return None

    if not 0 <= register <= 7:
        return None

    return register

def value_check(value):
    if len(value) < 3:
        try:
            value = int(value)
        except:
            return None
    elif value[:2] == '0b':
        try:
            value = int(value, 2)
        except:
            return None
    elif value[:2] == '0x':
        try:
            value = int(value, 16)
        except:
            return None
    else:
        try:
            value = int(value)
        except:
            return None

    if value < 0:
        return None

    return value


def analyze_message(message):
    separeted_message = message.lower().split()
    command = separeted_message[0]
    if command == "help":
        return HELP_MESSAGE
    elif command == "list":
        return tabulate([(k,) + v for k, v in DeviceManager().list_devices().items()], headers=['id', 'address', 'port'], tablefmt="outline") + f"\n Connected sensors: {len(DeviceManager().list_devices())}"
    # elif command == "ping":
    #     return ping_command(separeted_message)
    elif command == "read":
        return read_command(separeted_message)
    elif command == "config":
        return config_command(separeted_message)
    elif command == "exit":
        return EXIT_CODE
    else:
        return INVALID_COMMAND_MESSAGE
