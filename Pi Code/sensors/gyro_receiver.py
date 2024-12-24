import serial
import time

class GyroReceiver:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.is_connected = False

    def open_serial_port(self):
        """
        Opens the serial port for communication with the Bluetooth device.
        """
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.is_connected = True
            print(f"Successfully connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            self.is_connected = False

    def read_data(self):
        """
        Reads data from the serial port, if available.
        Returns the data as a string if available, otherwise None.
        """
        if not self.is_connected:
            print("Serial port not connected.")
            return None

        try:
            if self.serial_conn.in_waiting > 0:
                data = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                return data
            else:
                return None
        except serial.SerialException as e:
            print(f"Serial exception occurred: {e}")
            self.reconnect()
            return None
        except OSError as e:
            print(f"OSError occurred while reading data: {e}")
            self.reconnect()
            return None

    def reconnect(self):
        """
        Attempts to reconnect to the Bluetooth serial port in case of an error.
        """
        if self.serial_conn is not None:
            self.serial_conn.close()
        self.open_serial_port()

    def close(self):
        """
        Closes the serial port connection.
        """
        if self.serial_conn is not None:
            self.serial_conn.close()
            self.is_connected = False
            print("Connection closed.")
