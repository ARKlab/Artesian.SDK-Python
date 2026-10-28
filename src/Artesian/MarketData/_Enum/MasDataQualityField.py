from enum import Enum


class MasDataQualityField(Enum):
    Unspecified = 0
    Settlement = 1
    Open = 2
    Close = 3
    High = 4
    Low = 5
    VolumePaid = 6
    VolumeGiven = 7
    Volume = 8
