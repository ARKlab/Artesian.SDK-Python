from dataclasses import dataclass
import datetime
from typing import Optional
import dateutil


@dataclass
class CurveRangeEntity:
    """
        Class for the Curve Range Entity.
    """

    marketDataId: int = 0
    product: str = None
    version: str = None
    lastUpdated: datetime.datetime = datetime.datetime.min.replace(tzinfo=dateutil.tz.UTC)
    created: datetime.datetime = datetime.datetime.min.replace(tzinfo=dateutil.tz.UTC)
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None


    
