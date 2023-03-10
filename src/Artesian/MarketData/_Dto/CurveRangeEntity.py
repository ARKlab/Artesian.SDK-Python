from dataclasses import dataclass
import datetime
from typing import Optional
from dateutil import tz


@dataclass
class CurveRangeEntity:
    """
    Class for the Curve Range Entity.

    Attributes:
        marketDataId: the Market Data Identifier
        product: the product for MAS
        version: the version date for Versioned
        lastUpdated: Last Update for this curve
        created: Creation date for this curve
        rangeStart: start date of range for this curve
        rangeEnd: end date of range for this curve
    """

    marketDataId: int = 0
    product: Optional[str] = None
    version: Optional[str] = None
    lastUpdated: datetime.datetime = datetime.datetime.min.replace(tzinfo=tz.UTC)
    created: datetime.datetime = datetime.datetime.min.replace(tzinfo=tz.UTC)
    rangeStart: Optional[datetime.date] = None
    rangeEnd: Optional[datetime.date] = None
