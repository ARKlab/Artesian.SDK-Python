from dataclasses import dataclass
import datetime
from typing import Dict, Optional

from .MarketDataEntityOutput import MarketDataEntityOutput
from .DataQualityStatusSummaryDto import DataQualityStatusSummaryDto


@dataclass
class MarketDataCurveSummaryDto:
    """Summary information about the market data curve."""

    dataLastWritedAt: Optional[datetime.datetime] = None
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None


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
    curveSummary: Optional[MarketDataCurveSummaryDto] = None
