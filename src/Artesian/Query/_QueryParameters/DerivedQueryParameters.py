from __future__ import annotations
from typing import List, Optional
from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .VersionSelectionConfig import VersionSelectionConfig
from .ExtractionRangeType import ExtractionRangeType
from .VersionSelectionType import VersionSelectionType
from Artesian.MarketData import Granularity


class DerivedQueryParameters(_QueryParameters):
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
    """

    def __init__(
        self: DerivedQueryParameters,
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
    ) -> None:
        """
        Inits ActualQueryParameters

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
        """
        _QueryParameters.__init__(
            self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId
        )
        self.transformId = transformId
        self.granularity = granularity
        self.versionSelectionConfig = versionSelectionConfig or VersionSelectionConfig()
        self.versionSelectionType = versionSelectionType
        self.versionLimit = versionLimit
