from __future__ import annotations
from typing import List, Optional
from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .VersionSelectionConfig import VersionSelectionConfig
from .ExtractionRangeType import ExtractionRangeType
from .VersionSelectionType import VersionSelectionType
from Artesian.MarketData import Granularity
from Artesian.MarketData import AggregationRule


class VersionedQueryParameters(_QueryParameters):
    """
    Class for the Versioned Query Parameters.

    Attributes:
        ids: sets list of marketdata ID's to be queried
        extractionRangeConfig: Sets the extraction range configuration.
        extraxtionRangeType: Sets the extraction range type.
        timezone: specifies the timezone of extracted marketdata.
        filterId: filters marketdata ID to be queries.
        granularity: sets  the granularity to be queried.
        transformId: sets time range.
        versionSelectionConfig: Sets the version selectuon configuration.
        versionSelectionType: Sets the version selection time.
        unitOfMeasure: The UnitOfMeasure to use for extraction.
        aggregationRule: The AggregationRule to use for extraction.
    """

    def __init__(
        self: VersionedQueryParameters,
        ids: Optional[List[int]] = None,
        extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(),
        extractionRangeType: Optional[ExtractionRangeType] = None,
        timezone: Optional[str] = None,
        filterId: Optional[int] = None,
        granularity: Optional[Granularity] = None,
        transformId: Optional[str] = None,
        versionSelectionConfig: VersionSelectionConfig = VersionSelectionConfig(),
        versionSelectionType: Optional[VersionSelectionType] = None,
        versionLimit: Optional[str] = None,
        unitOfMeasure: Optional[str] = None,
        aggregationRule: Optional[AggregationRule] = None
    ) -> None:
        """
        Inits VersionedQueryParameters

        Args:

            ids: An int that ets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA. Specifies the timezone of extracted marketdata.
            filterId: An int that filters marketdata ID to be queries.
            granularity: An enum that sets  the granularity to be queried.
            transformId: An int that sets time range.
            versionSelectionConfig: Sets the version selectuon configuration.
            versionSelectionType: Sets the version selection time.
            unitOfMeasure: The UnitOfMeasure to use for extraction.
            aggregationRule: The AggregationRule to use for extraction.
        """
        _QueryParameters.__init__(
            self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId
        )
        self.transformId = transformId
        self.granularity = granularity
        self.versionSelectionConfig = versionSelectionConfig or VersionSelectionConfig()
        self.versionSelectionType = versionSelectionType
        self.versionLimit = versionLimit
        self.unitOfMeasure = unitOfMeasure
        self.aggregationRule = aggregationRule
