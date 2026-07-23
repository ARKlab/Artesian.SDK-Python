from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from .MarketDataEntityOutput import MarketDataEntityOutput


@dataclass
class MarketDataQualityRuleAssignmentDtoInput:
    """
    Write model for creating or updating a Market Data / Rule assignment.

    Attributes:
        id: unique identifier of this assignment, assigned by the server on
            creation
        marketDataId: identifier of the Market Data entity
        dataQualityRuleId: identifier of the Data Quality Rule
        eTag: entity tag for optimistic concurrency control
    """

    id: int = 0
    marketDataId: int = 0
    dataQualityRuleId: int = 0
    eTag: Optional[str] = None


@dataclass
class MarketDataQualityRuleAssignmentDtoOutput(MarketDataQualityRuleAssignmentDtoInput):
    """
    Read model returned by GET operations.

    Extends MarketDataQualityRuleAssignmentDtoInput with expanded navigation
    properties for Market Data and Data Quality Rule.

    Attributes:
        marketData: enriched Market Data entity associated with this assignment
        dataQualityRule: Data Quality Rule definition associated with this
            assignment, including aggregated status
        lookbackDate: lookback date from which data quality checks are
            evaluated for this assignment
        version: version number for concurrency tracking
    """

    marketData: Optional[MarketDataEntityOutput] = None
    dataQualityRule: Optional[DataQualityRuleDtoOutput] = None
    lookbackDate: Optional[datetime] = None
    version: int = 0
