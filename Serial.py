import serial.tools.list_ports
import time

MAX_CONNECTION_ATTEMPTS = 1000

class Serial:
    def __init__(self, baud: int):
        self.port = self.__find_port()
        self.serial = self.__connect(baud)

        received = ""
        while received != "RUTHERE":
            if not self.is_ready():
                print("Serial.py WAITING FOR SIGNAL")
                time.sleep(0.5)
            else:
                received = self.serial.readline().decode().strip()
        print(f"Serial.py FOUND SIGNAL: {received}")
        signal = b"ITSGOTIME"
        self.serial.write(signal)
        print(f"Serial.py: SENT SIGNAL: {signal.decode()}")
        self.serial.reset_input_buffer()

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
                if "ACM" in port.device or "COM" in port.device: 
                    return port.device
            print("Serial.py: Serial not found, retrying...")
            time.sleep(1)
    
    def write(self, message):
        self.serial.write(message.bytes())

    def close(self):
        try:
            self.serial.close()
        except:
            pass