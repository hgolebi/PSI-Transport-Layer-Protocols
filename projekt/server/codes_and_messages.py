HELP_MESSAGE = """
Available commands:
> help                              - shows available commands.
> list                              - shows list of available devices.
> read SENSOR_ID REGISTER           - reads value in the given register.
> config SENSOR_ID REGISTER VALUE   - sets register to the given value.
> exit                              - closes connection.
"""
START_MESSAGE = "Connected to the gateway." + HELP_MESSAGE
INVALID_COMMAND_MESSAGE = "Invalid command. Type 'help' to list available commands."
DEVICE_NOT_ACTIVE_MESSAGE = "Given device is not active.\nType 'list' to see all active devices."
WRONG_DEVICE_ID_MESSAGE = 'SENSOR_ID has to be a non-negative integer.'
WRONG_REGISTER_MESSAGE = '''REGISTER has to be a non-negative integer between 0 and 7.
For binary use '0b' before register number.
For hexadecimal use '0x' before register number.'''
WRONG_VALUE_MESSAGE = '''VALUE has to be a non-negative integer.
For binary use '0b' before register number.
For hexadecimal use '0x' before register number.'''
CONN_CLOSED_MESSAGE = "Connection closed."

# ERROR messages
SEND_ERROR = "Couldn't send the message."
CONNECTION_ERROR = 'Something went wrong during session.'
MESSAGE_SENT_INCORRECTLY_ERROR = 'Something went wrong while sending message to the device.'
DID_NOT_RECEIVE_DATA_ERROR = "Didn't receive any data from device."
VALUES_DOES_NOT_EQUAL_ERROR = "Devices response is different from the given value. There's a probability that the register hasn't been set properly."
DEVICE_STOPED_RESPONDING_ERROR = 'Device stopped responding.'

# ERROR CODES
EXIT_CODE = -1
DEVICE_NOT_ACTIVE_CODE = -2
MESSAGE_SENT_INCORRECTLY_CODE = -3
DID_NOT_RECEIVE_DATA_CODE = -4
VALUES_DOES_NOT_EQUAL_CODE = -5