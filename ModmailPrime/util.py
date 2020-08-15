from enum import Enum, auto


class StatusAction(Enum):
    OPEN = auto()
    CLOSED = auto()
    STALLED = auto()