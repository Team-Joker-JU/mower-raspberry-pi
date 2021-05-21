from enum import IntEnum

class RobotCommand(IntEnum):
    CONNECTED = 0,
    DISCONNECTED = 1,
    ACCELERATION = 2,
    STEERING = 3,
    COLLISION = 4,
    MODE = 5
