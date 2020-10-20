"""High-level enumerations for the pyaestro package."""


class EventCode(Enum):
    SUCCESS = 0
    FAILURE = 1


class TaskState(Enum):
    """An enumeration for task state."""
    BLOCKED = 0
    PENDING = 1
    WAITING = 2
    RUNNING = 3
    FINISHED = 4
    FAILED = 5
    INCOMPLETE = 6
    HWFAILURE = 7
    TIMEDOUT = 8
    UNKNOWN = 9
    CANCELLED = 10
