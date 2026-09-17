import serial.tools.list_ports
import time

MAX_CONNECTION_ATTEMPTS = 1000

class Serial:
    def __init__(self, baud: int):
        self.port = self.__find_port()
        self.serial = self.__connect(baud)

        print(f"Serial.py: FOUND SIGNAL: {self.serial.readline()}")

        signal = b"ITSGOTIME"
        self.serial.write(signal)
        print(f"Serial.py: SENT SIGNAL: {signal.decode()}")

    def __connect(self, baud):
        for attempt in range(MAX_CONNECTION_ATTEMPTS):
            try:
                ser = serial.Serial(self.port, baud, timeout=0)
                return ser
            except:
                print("Serial.py: Serial connection error, retrying...")
                self.port = self.__find_port()
                time.sleep(1)
        else:
            raise serial.SerialException("Too many connection attempts. Is serial connected?")

    def __find_port(self):
        while True:
            for port in serial.tools.list_ports.comports():
                if "ACM" in port.device:
                    return port.device
            print("Serial.py: Serial not found, retrying...")
            time.sleep(1)
    
    def is_ready(self):
        try: 
            if self.serial.in_waiting > 0:
                return True
            return False
        except (serial.SerialException, OSError):
            return False
    def read_country(self):
        try:
            data = self.serial.readline().decode().strip().capitalize()
            return data
        except (serial.SerialException, OSError):
            raise RuntimeError("Serial closed unexpectedly.")

    def close(self):
        try:
            self.serial.close()
        except:
            pass