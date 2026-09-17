import serial.tools.list_ports
import time

class Serial:
    
    def __init__(self, baud: int):
        self.port = self.__find_port()
        self.serial = serial.Serial(self.port, 9600, timeout=0)
    def __find_port(self):
        for port in serial.tools.list_ports.comports():
            if "ACM" in port.device:
                return port.device
        raise RuntimeError("No valid ACM port found.")

