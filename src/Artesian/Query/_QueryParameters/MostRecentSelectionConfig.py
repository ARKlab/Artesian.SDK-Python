from __future__ import annotations
from typing import Optional


class MostRecentSelectionConfig:
    """Class for Most Recent Selection Configuration.

    Attributes:
        dateStart: start date for most recent selection.
        dateEnd: end date for most recent selection.
        period: period for most recent selection.
        periodFrom: period start for most recent selection.
        periodTo: period end for most recent selection.
    """

    def __init__(
        self: MostRecentSelectionConfig,
        dateStart: Optional[str] = None,
        dateEnd: Optional[str] = None,
        period: Optional[str] = None,
        periodFrom: Optional[str] = None,
        periodTo: Optional[str] = None,
    ) -> None:
        """Inits for the Most Recent Selection Configuration."""
        self.dateStart: Optional[str] = dateStart
        """ Start date for most recent selection. (ISO format)"""
        self.dateEnd: Optional[str] = dateEnd
        """ End date for most recent selection. (ISO format)"""
        self.period: Optional[str] = period
        """ Period for most recent selection. (ISO format)"""
        self.periodFrom: Optional[str] = periodFrom
        """ Period start for most recent selection. (ISO format)"""
        self.periodTo: Optional[str] = periodTo
        """ Period end for most recent selection. (ISO format)"""
