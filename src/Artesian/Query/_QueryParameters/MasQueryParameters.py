from __future__ import annotations

from .ExtractionRangeConfig import ExtractionRangeConfig
from .ExtractionRangeType import ExtractionRangeType
from .QueryParameters import _QueryParameters


class MasQueryParameters(_QueryParameters):
    """
    Class for the Mas Query Parameters.

    Attributes:
        ids: sets list of marketdata ID's to be queried
        extractionRangeConfig: Sets the extraction range configuration.
        extraxtionRangeType: Sets the extraction range type.
        timezone: specifies the timezone of extracted marketdata.
        filterId: filters marketdata ID to be queries.
        products: sets products to be queried.
    """

    def __init__(
        self: MasQueryParameters,
        ids: list[int] | None = None,
        extractionRangeConfig: ExtractionRangeConfig | None = None,
        extractionRangeType: ExtractionRangeType | None = None,
        timezone: str | None = None,
        filterId: int | None = None,
        products: list[str] | None = None,
    ) -> None:
        """
        Inits MasQueryParameters

        Args:

            ids: An int that sets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA. A string that specifies the timezone of extracted data.
            filterId: An int that filters marketdata ID to be queries.
            products: A string that sets products to be queried.
        """
        _QueryParameters.__init__(self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId)
        self.products = products
