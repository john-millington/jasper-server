from enum import Enum

class RegressionType(Enum):
    ABSOLUTE = 1
    EQUIVALENT = 2
    DELTA_RANGE = 3
    EITHER = 4
    SCORE = 5
    DELTA = 6