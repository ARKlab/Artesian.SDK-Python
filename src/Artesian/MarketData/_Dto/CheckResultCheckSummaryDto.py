from dataclasses import dataclass
from typing import Optional
import datetime

from Artesian.MarketData._Dto.MarketDataQualityRuleAssignmentDto import MarketDataQualityRuleAssignmentDtoOutput


@dataclass
class CheckResultCheckSummaryDto:
    """
    CurveRange-like summary per data quality assignment.
    Provides a checksummary view with range metadata, modeled after CurveRangeV2.


    Attributes:
        assignment: The enriched assignment (expanded with OutputEnriched + Rule).
        lastCheckTime: Timestamp of the last quality check execution.
        product: Product identifier.
        version: Version timestamp (None for non-versioned time series).
        lastUpdated: Last time the check result was updated.
        created: Time when the check result was created.
        rangeStart: Start of the checked data range.
        rangeEnd: End of the checked data range.
        rangeExactStart: Exact start of the checked range (with time component).
        rangeExactEnd: Exact end of the checked range (with time component).
        aggregatedStatus: Aggregated quality status (OK = no issues, KO = failures detected).
        versionFrom: Version-from boundary for versioned time series (None for actuals).
    """
    lastCheckTime: datetime.datetime
    rangeStart: datetime.date
    rangeEnd: datetime.date
    aggregatedStatus: str
    assignment: Optional[MarketDataQualityRuleAssignmentDtoOutput] = None
    product: Optional[str] = None
    version: Optional[datetime.datetime] = None
    lastUpdated: Optional[datetime.datetime] = None
    created: Optional[datetime.datetime] = None
    rangeExactStart: Optional[datetime.datetime] = None
    rangeExactEnd: Optional[datetime.datetime] = None
    versionFrom: Optional[datetime.datetime] = None
