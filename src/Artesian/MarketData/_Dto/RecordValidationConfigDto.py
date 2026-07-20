from dataclasses import dataclass
from typing import Optional

from .._Enum.PeriodPrecision import PeriodPrecision


@dataclass
class RecordValidationConfigDto:
    """
    Defines the expected data presence window for a quality check.

    Specifies which time range of records should be validated and the
    granularity profile or calendar for determining expected slots.

    Attributes:
        recordRangeFrom: start offset relative to check execution time
            (Period in ISO format)
        recordRangeTo: end offset relative to check execution time
            (Period in ISO format)
        precision: optional truncation precision applied to cron
            reference time before Period offsets are evaluated
    """

    recordRangeFrom: str
    recordRangeTo: str
    precision: Optional[PeriodPrecision] = None
