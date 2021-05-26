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
            self.process_message_protocol();
           
    def write(self, packet: RobotPacket):
        print("Sending data to RobotSerial: " + str(packet.get_command()))
        self.serial.write(packet)
        
    def event_handler(self, packet: RobotPacket):
        self.write(packet)
        
    def process_message_protocol(self):
        if self.serial.in_waiting > 0:
            command = RobotCommand(int.from_bytes(self.serial.read(), "big"))
            
            #Implementera en "get_length" funktion
            bytes_to_read = {
                RobotCommand.CONNECTED: 0,
                RobotCommand.DISCONNECTED: 0,
                RobotCommand.ACCELERATION: 1,
                RobotCommand.STEERING: 1,
                RobotCommand.COLLISION: 1,
                RobotCommand.POSITION: 24
            }
            
            n = bytes_to_read.get(command);
            parameter = None

            if (n > 0):
                parameter = self.serial.read(n);
            
            packet = RobotPacket(command, parameter)
            self.event_queue.put(packet);
            
        