from __future__ import annotations
from typing import Optional
from Artesian.Query.RelativeInterval import RelativeInterval


class ExtractionRangeConfig:
    """This class sets up the Extraction Range Configuration.

    Attributes:
         dateStart: start day for the Date Range extraction.
         dateEnd: end date for the Date Range extraction.
         period: Period range for extraction.
         periodFrom: period start range for extraction.
         periodTo: period end range for extraction.
         relativeInterval: relative interval range for extraction.
    """

    def __init__(self: ExtractionRangeConfig) -> None:
        """Init for the Extraction Range Configuration."""
        self.dateStart: Optional[str] = None
        """ Start date for the Date Range for extraction. (ISO format) """
        self.dateEnd: Optional[str] = None
        """ End date for Date Renge for extraction. (ISO format)"""
        self.period: Optional[str] = None
        """ Period range for extraction. (ISO format)"""
        self.periodFrom: Optional[str] = None
        """ Period start range for extraction. (ISO format)"""
        self.periodTo: Optional[str] = None
        """ Period end range for extraction. (ISO format)"""
        self.relativeInterval: Optional[RelativeInterval] = None
        """ Relative Interval range for extraction."""
