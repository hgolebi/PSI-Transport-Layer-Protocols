
HELP_MESSAGE = '''
Available commands:
> help                              - shows available commands.
> ping SENSOR_ID                    - checks if sensor is available.
> read SENSOR_ID REGISTER           - reads value in the given register.
> config SENSOR_ID REGISTER VALUE   - sets register to the given value.
> exit                              - closes connection.
'''
EXIT_CODE = 1
INVALID_COMMAND_MESSAGE = "Invalid command. Type 'help' to list available commands."

def ping_command(message):
  pass

def read_command(message):
  pass

def config_command(message):
  pass

def invalid_command():
  pass

def analyze_message(message):
  separeted_message = message.lower().split()
  command = separeted_message[0]
  if command == 'help':
    return HELP_MESSAGE
  elif command == 'ping':
    return ping_command(separeted_message)
  elif command == 'read':
    return read_command(separeted_message)
  elif command == 'config':
    return config_command(separeted_message)
  elif command == 'exit':
    return EXIT_CODE
  else:
    return INVALID_COMMAND_MESSAGE