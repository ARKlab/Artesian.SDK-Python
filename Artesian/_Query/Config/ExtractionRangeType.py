from enum import Enum
class ExtractionRangeType(Enum):
    """ This class sets up the Extraction Range Type. """

    DATE_RANGE = 1
    PERIOD = 2
    PERIOD_RANGE = 3
    RELATIVE_INTERVAL = 4
