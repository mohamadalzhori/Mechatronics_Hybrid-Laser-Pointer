# run the file with "sudo -E python3 main.py"

from servo.s90 import S90Servo, S90Direction
from servo.mg90s import MG90SServo, MG90SDirection
from sensors.ir_listener import IRListener, IRKey
from sensors.gyro_receiver import GyroReceiver
from sensors.cv import CV
from modes import ControlMode
from config import *
from time import sleep
import threading

# Global variables for components
s90 = None
mg90s = None
ir = None
gyro = None
cv = None
current_mode = None
ir_command = None

def setup():
    global s90, mg90s, ir, gyro, current_mode, cv
    # Servos Initialization
    s90 = S90Servo(S90_PIN, MIN_ANGLE, MAX_ANGLE, CUSTOM_MIN_ANGLE, CUSTOM_MAX_ANGLE, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, MIDDLE_ANGLE, ANGLE_STEP)
    mg90s = MG90SServo(MG90S_PIN, MOVE_DURATION, FORWARD_PULSE, BACKWARD_PULSE, STOP_PULSE)

    # IR Listener Initialization
    ir = IRListener()

    # Gyro Receiver Initialization
    gyro = GyroReceiver(PORT, BAUDRATE, TIMEOUT)
    gyro.open_serial_port()
    
    # Computer Vision Initialization
    cv = CV()
     
    # Initial control mode
    current_mode = ControlMode.CV

def switch_mode():
        global current_mode, ir_command
        command = ir_command

        if  current_mode != ControlMode.IR and IRKey.IR_MODE_KEY.value == command:
            current_mode = ControlMode.IR
            print("Switching to IR mode...")
        elif current_mode != ControlMode.GYRO and IRKey.GYRO_MODE_KEY.value == command:
            current_mode = ControlMode.GYRO
            print("Switching to GYRO mode...")
        elif current_mode != ControlMode.CV and IRKey.CV_MODE_KEY.value == command:
            current_mode = ControlMode.CV
            print("Switching to CV mode...")   
            # Computer Vision mode not implemented yet.


def ir_control_loop():
    global ir_command
    command = ir_command

    if IRKey.UP.value == command:
        s90.move(S90Direction.UP)
        print("Key Up detected")
        ir_command = None
    elif IRKey.DOWN.value == command:
        s90.move(S90Direction.DOWN)
        print("Key Down detected")
        ir_command = None
    elif IRKey.FORWARD.value == command:
        mg90s.move(MG90SDirection.FORWARD)
        print("Key Forward detected")
        ir_command = None
    elif IRKey.BACKWARD.value == command:
        mg90s.move(MG90SDirection.BACKWARD)
        print("Key Backward detected")
        ir_command = None

        
def gyro_control_loop():
    gyro_data = gyro.read_data()
    if gyro_data is not None:
        if gyro_data == "Hard Right":
            mg90s.move(MG90SDirection.FORWARD)
            print("Gyro Hard Right detected")
        elif gyro_data == "Hard Left":
            mg90s.move(MG90SDirection.BACKWARD)
            print("Gyro Hard Left detected")
        elif gyro_data == "Hard Up":
            s90.move(S90Direction.UP)
            print("Gyro Hard Up detected")
        elif gyro_data == "Hard Down":
            s90.move(S90Direction.DOWN)
            print("Gyro Hard Down detected")
    

def read_ir():
    global ir_command
    for command in ir.listen():
        ir_command = command
        
        # Use regular expression to extract the key (starting with "KEY" and ending at space)
        match = re.search(r"KEY\S*", ir_command)
        
        if match:
            ir_command = match.group(0)  # Update ir_command to only the key
        else:
            ir_command = None  # Set to None or a default value if no key is found
        
        print(f"IR Command (Key only): {ir_command}")

def cv_control_loop():
    print("Computer Vision loop")
    for command in cv.see():
        print(command)

def main():
    global current_mode, ir_command
    try:
        ir_reading = threading.Thread(target=read_ir)
        ir_reading.daemon = True  # This makes the thread exit when the main program exits
        ir_reading.start()
 
        while True:  # Main loop, always checking both IR and Gyro
            if current_mode == ControlMode.IR:
                ir_control_loop()  # Call IR control loop
            elif current_mode == ControlMode.GYRO:
                gyro_control_loop()  # Call Gyro control loop
            elif current_mode == ControlMode.CV:
                cv_control_loop()
            switch_mode()
            sleep(0.1)  # Optional small delay for stability
   
    except KeyboardInterrupt:
        print("\nExiting main loop...")

def test():
    print("Test")
    cv = CV()
    for command in cv.see():
        print(command)
        
        
if __name__ == "__main__":
    setup()  # Initialize components
    main()   # Start the application


