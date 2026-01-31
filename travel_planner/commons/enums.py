from enum import Enum

class Intent(str, Enum):
    REQUEST = "request"
    INFORM = "inform"
    REJECT = "reject"
    ERROR = "error"