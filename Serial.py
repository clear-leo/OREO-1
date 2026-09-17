import serial.tools.list_ports
import time

class Serial:
    def __init__(self, baud: int):
        self.port = self.__find_port()
        self.serial = serial.Serial(self.port, baud, timeout=0)
        while self.serial.in_waiting < 1:
            print("WAITING FOR DEVICE...")
            time.sleep(0.1)
        print(f"FOUND SIGNAL: {self.serial.readline()}")
        signal = b"ITSGOTIME"
        self.serial.write(signal)
        print(f"SENT SIGNAL: {signal.decode()}")

    def __find_port(self):
        for port in serial.tools.list_ports.comports():
            if "ACM" in port.device:
                return port.device
        print("Serial not found, retrying...")
        time.sleep(1)
        port = self.__find_port()
        return port
    
    def is_ready(self):
        if self.serial.in_waiting > 1:
            return True
        return False
    def read_country(self):
        if not self.serial.is_open:
            raise serial.SerialException("Port not open")
        data = self.serial.readline().decode().strip().capitalize()
        return data 

    def close(self):
        try:
            self.serial.close()
        except Exception:
            pass
    
    def __enter__(self):
        return self
    def __exit__(self):
        self.close()