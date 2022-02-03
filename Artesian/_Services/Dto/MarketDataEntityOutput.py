from ArtesianTags import ArtesianTags
import datetime
from typing import Optional
from MarketDataEntityInput import MarketDataEntityInput

class MarketDataEntityOutput(MarketDataEntityInput):
    """ 
        Class for the Market Data Entity Output. 

        Attributes:
            lastUpdated: the last time the metadata has been updated
            dataLastWritedAt: the last time the data has been written at
            dataRangeStart: start date of range for this curve
            dataRangeEnd: end date of range for this curve
            created: the time the market data has been created
    """
    
    lastUpdated: datetime.datetime = datetime.datetime.min
    dataLastWritedAt: Optional[datetime.datetime] = None
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None
    created: datetime.datetime = datetime.datetime.min
    #tranform: missing due to handling class hierarchies deserializations