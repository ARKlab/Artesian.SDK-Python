from __future__ import annotations

from Artesian.MarketData import AggregationRule, Granularity

from .ExtractionRangeConfig import ExtractionRangeConfig
from .ExtractionRangeType import ExtractionRangeType
from .QueryParameters import _QueryParameters


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
        ids: list[int] | None = None,
        extractionRangeConfig: ExtractionRangeConfig | None = None,
        extractionRangeType: ExtractionRangeType | None = None,
        timezone: str | None = None,
        filterId: int | None = None,
        granularity: Granularity | None = None,
        transformId: str | None = None,
        unitOfMeasure: str | None = None,
        aggregationRule: AggregationRule | None = None,
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
        _QueryParameters.__init__(self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.unitOfMeasure = unitOfMeasure
        self.aggregationRule = aggregationRule
