# Helper from bluezero
from bluezero import async_tools

from queue import Queue

from robotpacket import RobotPacket
from robotcommand import RobotCommand
from robotstate import RobotState

import blepy

class RobotPeripheral(blepy.Peripheral):
    
    # Custom service UUID
    CPU_TMP_SRVC = '12341000-1234-1234-1234-123456789abc'
    
    def __init__(self, adapter_address, state: RobotState, event_queue: Queue):
        
        self.notifiers = {
            "Acceleration": None,
            "Steering": None,
            "Collision": None
        }
        
        self.event_queue = event_queue
        self.services = [RobotService(True, state, event_queue, self.notifiers)]
        super().__init__(self.services, adapter_address, "Robot", appearance=0)
    
    def _on_connect_callback(self, device):
        print("Connected to " + str(device.address))
        packet = RobotPacket(RobotCommand.CONNECTED)
        self.event_queue.put(packet)
           
    def _on_disconnect_callback(self, adapter_address, device_address):
        print("Disconnected from " + device_address)
        packet = RobotPacket(RobotCommand.DISCONNECTED)
        self.event_queue.put(packet)
        
    def event_handler(self, packet: RobotPacket):
        switcher = {
            RobotCommand.ACCELERATION: self.notifiers["Acceleration"],
            RobotCommand.STEERING: self.notifiers["Steering"],
            RobotCommand.COLLISION: self.notifiers["Collision"]
        }

        notifier = switcher.get(packet.get_command())
        if notifier is not None:
            notifier.set_value(list(packet.get_parameter().to_bytes(1, byteorder='little', signed=True)))

class RobotService(blepy.Service):
    
    # Custom service UUID
    CPU_TMP_SRVC = '12341001-1234-1234-1234-123456789abc'
    
    def __init__(self, primary, state: RobotState, event_queue: Queue, notifiers: map):
        super().__init__(self.CPU_TMP_SRVC, primary)   
        self.characteristics = [
            RobotCharacteristics.Acceleration(state, event_queue, notifiers),
            RobotCharacteristics.Steering(state, event_queue, notifiers),
            RobotCharacteristics.Collision(state, event_queue, notifiers),
            RobotCharacteristics.Automove(state, event_queue, notifiers),
        ]

class RobotCharacteristics:
    
    class Acceleration(blepy.Characteristic):
        
        def __init__(self, state: RobotState, event_queue: Queue, notifiers: map):
            super().__init__("12341002-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['write']
            self.write_callback = self.write
            self.state = state
            
        def write(self, value, options):
            packet = RobotPacket(RobotCommand.ACCELERATION, int.from_bytes(value, byteorder='little', signed=True))
            self.event_queue.put(packet)
    
    
    class Steering(blepy.Characteristic):
        
        def __init__(self, state: RobotState, event_queue: Queue, notifiers: map):
            super().__init__("12341003-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['write']
            self.write_callback = self.write
            self.state = state
            
        def write(self, value, options):
            packet = RobotPacket(RobotCommand.STEERING, int.from_bytes(value, byteorder='little', signed=True))
            self.event_queue.put(packet)


    class Collision(blepy.Characteristic):
        
        def __init__(self, state: RobotState, event_queue: Queue, notifiers: map):
            super().__init__("12341004-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['notify']
            self.notify_callback = self.notify
            self.notifiers = notifiers
        
        def notify(self, notifying, characteristic):
            self.notifiers["Collision"] = characteristic if notifying else None
            return notifying

    class Automove(blepy.Characteristic):
        
        def __init__(self, state: RobotState, event_queue: Queue, notifiers: map):
            super().__init__("12341005-1234-1234-1234-123456789abc", event_queue)
            self.flags = ['write']
            self.write_callback = self.write
            self.notifiers = notifiers
        
        def write(self, value, options):
            packet = RobotPacket(RobotCommand.MODE)
            self.event_queue.put(packet)

