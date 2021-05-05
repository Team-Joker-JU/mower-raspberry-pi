from robotpacket import RobotPacket
from robotcommand import RobotCommand

import serial
import time

class RobotSerial:
    def __init__(self, port, baudrate, timeout, event_queue):
        self.event_queue = event_queue
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        self.serial.flush()
    # use Threading Event??
    def begin(self):
        while True:
            time.sleep(50)
            if self.serial.in_waiting > 0:
                print("Received data from RobotSerial: " + str(self.serial.readline()))
           
    def write(self, packet: RobotPacket):
        print("Sending data to RobotSerial: " + str(packet.get_command()))
        self.serial.write(packet)
        
    def event_handler(self, packet: RobotPacket):
        self.write(packet);