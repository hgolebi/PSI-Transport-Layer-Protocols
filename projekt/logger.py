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

    def log(self, message):
        log_record = f"{self.get_time()} {message}\n"
        print(message)
        self.file = open(self.file_path, "a")
        self.file.write(log_record)
        self.file.close()
