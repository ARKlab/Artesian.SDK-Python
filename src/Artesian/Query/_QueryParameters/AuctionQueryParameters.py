from __future__ import annotations
from typing import List, Optional
from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .ExtractionRangeType import ExtractionRangeType


class AuctionQueryParameters(_QueryParameters):
    """
    Class for the Auction Query Parameters.

    Attributes:
        ids: sets list of marketdata ID's to be queried
        extractionRangeConfig: Sets the extraction range configuration.
        extraxtionRangeType: Sets the extraction range type.
        timezone: pecifies the timezone of extracted marketdata.
        filterId: filters marketdata ID to be queries.
    """

    def __init__(
        self: AuctionQueryParameters,
        ids: Optional[List[int]] = None,
        extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(),
        extractionRangeType: Optional[ExtractionRangeType] = None,
        timezone: Optional[str] = None,
        filterId: Optional[int] = None,
    ) -> None:
        """
        Inits AuctionQueryParameters

        Args:

            ids: An int that sets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA. A string that specifies the timezone of extracted data.
            filterId: An int that filters marketdata ID to be queries.
        """
        _QueryParameters.__init__(
            self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId
        )
