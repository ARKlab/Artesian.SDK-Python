from ArtesianTags import ArtesianTags
import datetime
from typing import Optional
from MarketDataEntityInput import MarketDataEntityInput

class MarketDataEntityOutput(MarketDataEntityInput):
    """ Class for the Market Data Entity Output. """
    lastUpdated: datetime.datetime = datetime.datetime.min
    dataLastWritedAt: Optional[datetime.datetime] = None
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None
    created: datetime.datetime = datetime.datetime.min
    #tranform: missing due to handling class hierarchies deserializations