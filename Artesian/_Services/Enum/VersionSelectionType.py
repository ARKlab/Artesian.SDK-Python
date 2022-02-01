from enum import Enum
class VersionSelectionType(Enum):
    LastN =  1
    Muv = 2
    LastOfDays = 3
    LLastOfMonths = 4
    Version = 5
    MostRecent = 6