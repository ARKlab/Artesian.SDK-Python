from __future__ import annotations


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
        dateStart: str | None = None,
        dateEnd: str | None = None,
        period: str | None = None,
        periodFrom: str | None = None,
        periodTo: str | None = None,
    ) -> None:
        """Inits for the Most Recent Selection Configuration."""
        self.dateStart: str | None = dateStart
        """ Start date for most recent selection. (ISO format)"""
        self.dateEnd: str | None = dateEnd
        """ End date for most recent selection. (ISO format)"""
        self.period: str | None = period
        """ Period for most recent selection. (ISO format)"""
        self.periodFrom: str | None = periodFrom
        """ Period start for most recent selection. (ISO format)"""
        self.periodTo: str | None = periodTo
        """ Period end for most recent selection. (ISO format)"""
