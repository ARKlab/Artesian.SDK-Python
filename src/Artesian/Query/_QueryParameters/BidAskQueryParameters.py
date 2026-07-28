from __future__ import annotations
from typing import List, Optional
from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .ExtractionRangeType import ExtractionRangeType


class BidAskQueryParameters(_QueryParameters):
    """
    Class for the Bid Ask Query Parameters.

    Attributes:
        ids: sets list of marketdata ID's to be queried
        extractionRangeConfig: Sets the extraction range configuration.
        extraxtionRangeType: Sets the extraction range type.
        timezone:specifies the timezone of extracted marketdata.
        filterId: filters marketdata ID to be queries.
        products: sets products to be queried.
    """

    def __init__(
        self: BidAskQueryParameters,
        ids: Optional[List[int]] = None,
        extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(),
        extractionRangeType: Optional[ExtractionRangeType] = None,
        timezone: Optional[str] = None,
        filterId: Optional[int] = None,
        products: Optional[List[str]] = None,
    ) -> None:
        """
        Inits BidAskQueryParameters

        Args:

            ids: An int that sets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA. A string that specifies the timezone of extracted data.
            filterId: An int that filters marketdata ID to be queries.
            products: A string that sets products to be queried.
        """
        _QueryParameters.__init__(
            self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId
        )
        self.products = products
