from __future__ import annotations


class ExtractionRangeConfig:
    """
    Class for the Extraction Range Configuration.

    Attribute:
        date: Date for the Extraction Range configuration in (ISO) format
    """

    def __init__(self: ExtractionRangeConfig, date: str | None = None) -> None:
        """Inits the Extraction Range Configuration."""
        self.date = date
