from enum import Enum


class Granularity(Enum):
    Hour = 0
    Day = 1
    Week = 2
    Month = 3
    Quarter = 4
    Year = 5
    TenMinute = 6
    FifteenMinute = 7
    Minute = 8
    ThirtyMinute = 9
