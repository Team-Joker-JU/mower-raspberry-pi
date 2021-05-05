from enum import IntEnum

class RobotCommand(IntEnum):
    HANDSHAKE = 0,
    CONNECTED = 1,
    RECIEVED  = 2,
    ACCELERATION = 3,
    STEERING = 4,
    COLLISION = 5
