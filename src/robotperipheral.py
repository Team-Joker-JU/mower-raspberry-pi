from robotpacket import RobotPacket
from robotcommand import RobotCommand

import blepy

class RobotPeripheral(blepy.Peripheral):
    
    # Custom service UUID
    CPU_TMP_SRVC = '12341000-1234-1234-1234-123456789abc'
    
    def __init__(self, adapter_address, robot, event_queue): 
        self.services = [RobotService(True, robot, event_queue)]
        super().__init__(self.services, adapter_address, "Robot", appearance=0)

class RobotService(blepy.Service):
    
    # Custom service UUID
    CPU_TMP_SRVC = '12341001-1234-1234-1234-123456789abc'
    
    def __init__(self, primary, robot, event_queue):
        super().__init__(self.CPU_TMP_SRVC, primary)   
        self.characteristics = [
            RobotCharacteristics.Handshake(robot, event_queue),
            RobotCharacteristics.Acceleration(robot, event_queue)
        ]


class RobotCharacteristics:
    
    class Handshake(blepy.Characteristic):
        
        def __init__(self, robot, event_queue):
            super().__init__("12341002-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['write', 'read', 'notify']
            self.write_callback = self.write
            self.read_callback = self.read
            self.notify_callback = self.notify
            self.robot = robot
        
        def read(self):
            return list(int(self.robot.is_paired).to_bytes(1, byteorder='little', signed=True))
        
        def notify(self, notifying, characteristic):
            characteristic.set_value(self.read())
            return notifying
        
        def write(self, value, options):
            packet = RobotPacket(RobotCommand.HANDSHAKE)
            self.event_queue.put(packet)
        
    class Acceleration(blepy.Characteristic):
        
        def __init__(self, robot, event_queue):
            super().__init__("12341003-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['write']
            self.write_callback = self.write

        def write(self, value, options):
            packet = RobotPacket(RobotCommand.ACCELERATION, int.from_bytes(value, byteorder='little', signed=True))
            self.event_queue.put(packet)


