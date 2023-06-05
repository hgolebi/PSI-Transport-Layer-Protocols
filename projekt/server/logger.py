"""
Brama komunikacyjna dla urządzeń sensorycznych
Hubert Gołębiowski, Bartosz Pomiankiewicz, Bartłomiej Rodzik
26.05.2023
"""
import os
from datetime import datetime


class Logger:
    def __init__(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        time = str(datetime.now())
        self.file_path = "logs/log_" + time.replace(" ", "_").replace(":", "-") + ".txt"

    @staticmethod
    def get_time():
        return "[" + str(datetime.now()) + "]"

    @staticmethod
    def _ansi(number):
        return '\033[' + str(number) + 'm'

    def log(self, message):
        log_time = self.get_time()
        log_record = f"{message}"
        print(log_record)
        self.file = open(self.file_path, "a")
        self.file.write(f"{log_time} {log_record}\n")
        self.file.close()
    
    def error(self, message):
        log_time = self.get_time()
        log_record = f"ERROR: {message}"
        print(self._ansi(91) + log_record + self._ansi(0))
        self.file = open(self.file_path, "a")
        self.file.write(f"{log_time} {log_record}\n")
        self.file.close()
