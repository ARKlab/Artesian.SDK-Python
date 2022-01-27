from enum import Enum
class VersionSelectionType(Enum):
    """ This class sets the Version Selection Type.
    """
    LASTN =  1
    MUV = 2
    LAST_OF_DAYS = 3
    LAST_OF_MONTHS = 4
    VERSION = 5
    MOST_RECENT = 6