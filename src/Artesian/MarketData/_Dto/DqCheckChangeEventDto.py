from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .._Enum.CheckAggregatedStatus import CheckAggregatedStatus


@dataclass
class LocalDateTimeRange:
    """
    Represents an impacted time range with start inclusive and end exclusive.

    Attributes:
        start: start timestamp (inclusive)
        end: end timestamp (exclusive)
    """

    start: Optional[datetime] = None
    end: Optional[datetime] = None


@dataclass
class DqCheckChangeEventDtoOutput:
    """
    Output model for data quality check change events.

    Attributes:
        marketDataId: identifier of the Market Data entity
        ruleId: identifier of the Data Quality Rule
        assignmentId: identifier of the assignment binding rule to market data
        version: version timestamp for versioned time series, None for actual
        product: product identifier within the market data curve
        rangeImpacted: impacted time range (start inclusive, end exclusive)
        newStatus: new aggregated check status after the change
        oldStatus: previous aggregated check status, None for first check
        timestamp: instant when this status change occurred
        ruleName: human-readable Data Quality Rule name
        ruleVersion: rule configuration version at check time
        marketDataName: Market Data entity name
        provider: Market Data entity provider
    """

    marketDataId: int = 0
    ruleId: int = 0
    assignmentId: int = 0
    version: Optional[datetime] = None
    product: Optional[str] = None
    rangeImpacted: Optional[LocalDateTimeRange] = None
    newStatus: Optional[CheckAggregatedStatus] = None
    oldStatus: Optional[CheckAggregatedStatus] = None
    timestamp: Optional[datetime] = None
    ruleName: Optional[str] = None
    ruleVersion: int = 0
    marketDataName: Optional[str] = None
    provider: Optional[str] = None
