import blepy

from queue import Queue
from threading import Thread, Event

from robotperipheral import RobotPeripheral
from robotserial     import RobotSerial
from robotstate      import RobotState
class Controller:
    
    state            = RobotState()
    queue_peripheral = Queue(maxsize=0)
    queue_serial     = Queue(maxsize=0)
    
    def __init__(self):
        
        self.peripheral = RobotPeripheral(blepy.Adapter.get_available_address(), self.state, self.queue_peripheral)
        self.serial     = RobotSerial('/dev/ttyACM0', 9600, 1, self.state, self.queue_serial)
        
        self.workers = [
            Thread(target=self.peripheral.publish),
            Thread(target=self.serial.begin),
            Thread(target=self._queue_work, args=[self.queue_peripheral, self.serial.event_handler]),
            Thread(target=self._queue_work, args=[self.queue_serial, None])
        ]
    
    def start(self):
        for w in self.workers:
            w.setDaemon(True)
            w.start()
        
        for w in self.workers:
            w.join()
        
    def _queue_work(self, q, handler):
        while True:
            event = q.get()
            handler(event)