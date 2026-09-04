from dataclasses import dataclass
from typing import List, Optional

from Artesian.MarketData._Dto.DataQualityStatusSummaryDto import DataQualityStatusSummaryDto
from Artesian.MarketData._Dto.MarketDataEntityOutputEnriched import MarketDataEntityOutputEnriched


@dataclass
class MarketDataDqStatusSummaryDto:
    """
    DTO pairing a Market Data entity with its aggregated DQ status summary,
    its full enriched Market Data entity and the list of rule assignments
    (carrying LookbackDate) for the Data Quality overview.
    Used by the MarketData DQ Status Summary endpoint.

    Attributes:
        marketDataId: The Market Data entity identifier.
        statusSummary: The aggregated DQ status summary for this Market Data under the queried rule.
        marketData: The full enriched Market Data entity. None if no rule assignment exists for this Market Data.
        assignments: The Data Quality rule assignments bound to this Market Data (respecting the queried rule filter).
    """
    marketDataId: int
    statusSummary: Optional[DataQualityStatusSummaryDto] = None
    marketData: Optional[MarketDataEntityOutputEnriched] = None
    assignments: Optional[List] = None
