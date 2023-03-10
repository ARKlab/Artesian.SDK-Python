from enum import Enum


class ExtractionRangeType(Enum):
    DateRange = 1
    Period = 2
    PeriodRange = 3
    RelativeInterval = 4
