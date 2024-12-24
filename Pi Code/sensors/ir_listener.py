import subprocess
from enum import Enum

class IRKey(Enum):
    UP = "KEY_VOLUMEUP"
    DOWN = "KEY_VOLUMEDOWN"
    FORWARD = "KEY_NEXT"
    BACKWARD = "KEY_PREVIOUS"
    IR_MODE_KEY = "KEY_1"
    GYRO_MODE_KEY = "KEY_2"
    CV_MODE_KEY = "KEY_PLAYPAUSE"

class IRListener:
    def __init__(self):
        self.process = subprocess.Popen(['irw'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def listen(self):
        while True:
            line = self.process.stdout.readline().strip()
            yield line
