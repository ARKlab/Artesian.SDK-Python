from enum import Enum
class Granularity(Enum):

    """ Class that sets the Granularity to be queried.
    
    The time granularity should always be specified.
    """
    HOUR = 0
    DAY = 1
    WEEK = 2
    MONTH = 3
    QUARTER = 4
    YEAR = 5
    TEN_MINUTE = 6
    FIFTEEN_MINUTE = 7
    MINUTE = 8
    THIRTY_MINUTE = 9
    