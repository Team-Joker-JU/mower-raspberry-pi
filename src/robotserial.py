from queue import Queue

from robotpacket import RobotPacket
from robotcommand import RobotCommand
from robotstate import RobotState

import serial

class RobotSerial:
    def __init__(self, port, baudrate, timeout, state: RobotState, event_queue: Queue):
        self.event_queue = event_queue
        self.state = state
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        self.serial.flush()
    # use Threading Event??
    def begin(self):
        while True:
            # delay?
            if self.serial.in_waiting > 0:
                print("Received data from RobotSerial: " + str(self.serial.readline()))
           
    def write(self, packet: RobotPacket):
        print("Sending data to RobotSerial: " + str(packet.get_command()))
        self.serial.write(packet)
        
    def event_handler(self, packet: RobotPacket):
        self.write(packet);