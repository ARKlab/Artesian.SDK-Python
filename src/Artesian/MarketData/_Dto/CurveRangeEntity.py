import datetime
from dataclasses import dataclass

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
    product: str | None = None
    version: str | None = None
    lastUpdated: datetime.datetime = datetime.datetime.min.replace(tzinfo=tz.UTC)
    created: datetime.datetime = datetime.datetime.min.replace(tzinfo=tz.UTC)
    rangeStart: datetime.date | None = None
    rangeEnd: datetime.date | None = None
