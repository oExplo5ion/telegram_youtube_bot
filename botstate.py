from enum import Enum

class BotState(Enum):
    IDLE = 0
    WAITING_FOR_LINK = 1
    WAITING_FOR_RESOLUTION = 2