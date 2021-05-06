import struct
from typing import Callable

from robotcommand import RobotCommand

class RobotPacket(bytearray):
    def __init__(self, command: RobotCommand, parameter: int = None):
        self.extend(self._to_int8_bytearray(command))
        
        if parameter is not None:
            self.extend(self._to_int_switch(command)(parameter))
    
    def get_command(self) -> RobotCommand:
        return RobotCommand(struct.unpack('<b', self[0:1])[0])
    
    def get_parameter(self) -> int:
        # Denna borde fixas
        return struct.unpack('<l', self[1:5])[0]
    
    def _to_int_switch(self, command: RobotCommand) -> Callable:
        return {
            RobotCommand.ACCELERATION: self._to_int8_bytearray,
            RobotCommand.STEERING: self._to_int8_bytearray
        }[command]
    
    def _to_int8_bytearray(self, value):
        return struct.pack('<b', value)
    
    def _to_int16_bytearray(self, value):
        return struct.pack('<h', value)
    
    def _to_int32_bytearray(self, value):
        return struct.pack('<l', value)