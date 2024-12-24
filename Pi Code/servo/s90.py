from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from enum import Enum

class S90Direction(Enum):
    UP = "up"
    DOWN = "down"

class S90Servo:
    def __init__(self, pin, min_angle, max_angle, custom_min_angle, custom_max_angle, min_pulse_width, max_pulse_width, middle_angle, angle_step):
        factory = PiGPIOFactory()
        self.servo = AngularServo(pin, 
                                  min_angle=min_angle, 
                                  max_angle=max_angle, 
                                  min_pulse_width=min_pulse_width, 
                                  max_pulse_width=max_pulse_width, 
                                  pin_factory=factory)
        self.current_angle = middle_angle
        self.servo.angle = self.current_angle

        self.custom_min_angle = custom_min_angle
        self.custom_max_angle = custom_max_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle_step = angle_step

    def move(self, direction: S90Direction):
        if direction == S90Direction.UP:
            self.current_angle += self.angle_step
        elif direction == S90Direction.DOWN:
            self.current_angle -= self.angle_step

        self.current_angle = max(max(self.min_angle, self.custom_min_angle), min(min(self.max_angle, self.custom_max_angle), self.current_angle))
        self.servo.angle = self.current_angle
        print(f"S90 Servo angle set to: {self.current_angle}")
