from dataclasses import dataclass
from typing import Dict, Optional, Any

from .MarketDataEntityOutput import MarketDataEntityOutput
from .DataQualityStatusSummaryDto import DataQualityStatusSummaryDto


@dataclass
class MarketDataEntityOutputEnriched(MarketDataEntityOutput):
    """
    The MarketData Output Enriched with additional optional information.

    Attributes:
        dataQualityStatusSummary: The latest data quality status summary per rule type.
            Populated when includeDataQuality=true.
        curveSummary: CurveSummary info about the market data.
            Populated when includeCurveSummary=true.
    """
    dataQualityStatusSummary: Optional[Dict[str, DataQualityStatusSummaryDto]] = None
    curveSummary: Optional[Any] = None
