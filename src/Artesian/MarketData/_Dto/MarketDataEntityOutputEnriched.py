import datetime
from dataclasses import dataclass

from .DataQualityStatusSummaryDto import DataQualityStatusSummaryDto
from .MarketDataEntityOutput import MarketDataEntityOutput


@dataclass
class MarketDataCurveSummaryDto:
    """Summary information about the market data curve."""

    dataLastWritedAt: datetime.datetime | None = None
    dataRangeStart: datetime.date | None = None
    dataRangeEnd: datetime.date | None = None


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

    dataQualityStatusSummary: dict[str, DataQualityStatusSummaryDto] | None = None
    curveSummary: MarketDataCurveSummaryDto | None = None
