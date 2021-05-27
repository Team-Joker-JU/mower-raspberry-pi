import blepy

from queue import Queue
from threading import Thread, Event

from robotperipheral import RobotPeripheral
from robotserial     import RobotSerial
from robotstate      import RobotState
from robotpacket     import RobotPacket
from robotcommand    import RobotCommand
import requests
import json

class Controller:
    
    state            = RobotState()
    queue_peripheral = Queue(maxsize=0)
    queue_serial     = Queue(maxsize=0)
    
    def __init__(self, usb_port: str, baud_rate: int):
        self.peripheral = RobotPeripheral(blepy.Adapter.get_available_address(), self.state, self.queue_peripheral)
        self.serial     = RobotSerial(usb_port, baud_rate, 1, self.state, self.queue_serial)
        self.workers = [
            Thread(target=self.peripheral.publish),
            Thread(target=self.serial.begin),
            Thread(target=self._queue_work, args=[self.queue_peripheral, self.serial.event_handler]),
            Thread(target=self._queue_work, args=[self.queue_serial, self.peripheral.event_handler]),
            Thread(target=self._queue_work, args=[self.queue_serial, self._local_event_handler]),
        ]
    
    def start(self):
        for w in self.workers:
            w.setDaemon(True)
            w.start()
        
        for w in self.workers:
            w.join()
            
    def createRequest(self, x, y):
        API_ENDPOINT = 'https://ims_api.supppee.workers.dev/api/coord/'
        
        data = {
            "session": "Hej emil",
            "collision": False,
            "X": x,
            "Y": y,
        }
        
        print(data)
        
        r = requests.post(url = API_ENDPOINT, data = json.dumps(data))
    
    
    def _local_event_handler(self, packet: RobotPacket):
        if (packet.get_command() == RobotCommand.POSITION):
            xAndY = packet.get_parameter().split("~")
            x = float(xAndY[0][0:4])
            y = float(xAndY[1][0:4])
            self.createRequest(x, y)
        
    
    def _queue_work(self, q, handler):
        while True:
            event = q.get()
            handler(event)
            
   