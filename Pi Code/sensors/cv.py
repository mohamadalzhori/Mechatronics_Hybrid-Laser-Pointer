import subprocess
import threading
import queue
import sys
import os

class CV():
    def __init__(self):
        self.pipe_path = "/tmp/movement_commands"
        self.create_pipe()
        self.run_libcamera_vid()
        self.run_detect_script()

    def create_pipe(self):
        # Create the named pipe if it doesn't exist
        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)
    
    def run_libcamera_vid(self):
        # Command to run libcamera-vid
        command = [
            "libcamera-vid", "-n", "-t", "0",
            "--width", "426", "--height", "240",
            "--framerate", "30", "--inline",
            "--listen", "-o", "tcp://127.0.0.1:8888"
        ]
        # Run the command and suppress its output
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def run_detect_script(self):
        # Command to run the detect.py script with the desired arguments
        command = [
            "xvfb-run", "-a", "python3", "detect.py",
            "--source", "tcp://127.0.0.1:8888",
            "--weights", "yolov5n.pt",
            "--classes", "39",
            "--conf-thres", "0.05"
        ]
        # Run the command and suppress its output, .../yolov5 is the path to the yolov5 directory
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd="../yolov5")


    def see(self):
        # Open the named pipe for reading
        with open(self.pipe_path, 'r') as pipe:
            while True:
                command = pipe.readline().strip()
                if command:
                    yield command
