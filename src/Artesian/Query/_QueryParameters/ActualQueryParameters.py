from __future__ import annotations
from typing import List, Optional
from .QueryParameters import _QueryParameters
from .ExtractionRangeType import ExtractionRangeType
from .ExtractionRangeConfig import ExtractionRangeConfig
from Artesian.MarketData import Granularity
from Artesian.MarketData import AggregationRule


class ActualQueryParameters(_QueryParameters):
    """
    Class for the Actual Query Parameters.

    Attributes:
        ids: sets list of marketdata ID's to be queried
        extractionRangeConfig: Sets the extraction range configuration.
        extractionRangeType: Sets the extraction range type.
        timezone: specifies the timezone of extracted marketdata.
        filterId: filters marketdata ID to be queries.
        granularity: sets  the granularity to be queried.
        transformId: sets time range.
        unitOfMeasure: The UnitOfMeasure to use for extraction.
        aggregationRule: The AggregationRule to use for extraction.
    """

    def __init__(
        self: ActualQueryParameters,
        ids: Optional[List[int]] = None,
        extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(),
        extractionRangeType: Optional[ExtractionRangeType] = None,
        timezone: Optional[str] = None,
        filterId: Optional[int] = None,
        granularity: Optional[Granularity] = None,
        transformId: Optional[str] = None,
        unitOfMeasure: Optional[str] = None,
        aggregationRule: Optional[AggregationRule] = None
    ) -> None:
        """
        Inits ActualQueryParameters

        Args:

            ids: An int that sets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA. A string that specifies the timezone of extracted data.
            filterId: An int that filters marketdata ID to be queries.
            granularity: An enum that sets  the granularity to be queried.
            transformId: The name of the Time Transform to use for extraction.
            unitOfMeasure: The UnitOfMeasure to use for extraction.
            aggregationRule: The AggregationRule to use for extraction.
        """
        _QueryParameters.__init__(
            self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId
        )
        self.granularity = granularity
        self.transformId = transformId
        self.unitOfMeasure = unitOfMeasure
        self.aggregationRule = aggregationRule
