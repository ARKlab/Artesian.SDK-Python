from dataclasses import dataclass
import datetime
from typing import Optional
from zoneinfo import ZoneInfo


@dataclass
class CurveRangeEntity:
    """
        Class for the Curve Range Entity.
    """

    marketDataId: int = 0
    product: str = None
    version: str = None
    lastUpdated: datetime.datetime = datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC'))
    created: datetime.datetime = datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC'))
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None


    
