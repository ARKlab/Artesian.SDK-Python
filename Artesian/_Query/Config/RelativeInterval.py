from enum import Enum
class RelativeInterval(Enum):
    ROLLING_WEEK =  1
    ROLLING_MONTH = 2
    ROLLING_QUARTER = 3
    ROLLING_YEAR = 4
    WEEK_TO_DATE = 5
    MONTH_TO_DATE = 6
    QUARTER_TO_DATE = 7
    YEAR_TO_DATE = 8
