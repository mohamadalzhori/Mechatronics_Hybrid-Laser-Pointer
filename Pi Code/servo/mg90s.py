import pigpio
from time import sleep
from enum import Enum

class MG90SDirection(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"

class MG90SServo:
    def __init__(self, pin, duration, forward_pulse, backward_pulse, stop_pulse):
        self.pi = pigpio.pi()
        self.pin = pin
        self.duration = duration
        self.forward_pulse = forward_pulse
        self.backward_pulse = backward_pulse
        self.stop_pulse = stop_pulse

    def move(self, direction: MG90SDirection):
        if direction == MG90SDirection.FORWARD:
            self.pi.set_servo_pulsewidth(self.pin, self.forward_pulse)
        elif direction == MG90SDirection.BACKWARD:
            self.pi.set_servo_pulsewidth(self.pin, self.backward_pulse)
        sleep(self.duration)
        self.pi.set_servo_pulsewidth(self.pin, self.stop_pulse)  # Stop pulse
