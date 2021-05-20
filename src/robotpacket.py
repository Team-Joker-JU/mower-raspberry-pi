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
        unpacker = {
            RobotCommand.ACCELERATION: self._to_int8,
            RobotCommand.STEERING: self._to_int8,
            RobotCommand.COLLISION: self._to_int8
        }
        
        unpack = unpacker.get(self.get_command())
        return unpack(self, 1)
    
    def _to_int_switch(self, command: RobotCommand) -> Callable:
        return {
            RobotCommand.ACCELERATION: self._to_int8_bytearray,
            RobotCommand.STEERING: self._to_int8_bytearray,
            RobotCommand.COLLISION: self._to_int8_bytearray
        }[command]
    
    def _to_int8_bytearray(self, value):
        return struct.pack('<b', value)
    
    def _to_int16_bytearray(self, value):
        return struct.pack('<h', value)
    
    def _to_int32_bytearray(self, value):
        return struct.pack('<l', value)
    
    def _to_int8(self, value, offset):
        return struct.unpack('<b', value[offset:offset+1])[0]
    
    def _to_int16(self, value, offset):
        return struct.unpack('<h', value[offset:offset+2])[0]
    
    def _to_int32(self, value, offset):
        return struct.unpack('<l', value[offset:offset+4])[0]