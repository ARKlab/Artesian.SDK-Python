from typing import List, Optional
from Artesian.Granularity import Granularity
from .ExtractionRangeConfig import ExtractionRangeConfig
from .ExtractionRangeType import ExtractionRangeType

class _FillStrategy:
    def getUrlParams(self) -> str:
        raise NotImplementedError("Please Implement this method")

class _NullFillStrategy(_FillStrategy):
    def getUrlParams(self):
        return "fillerK=Null"

class _NoFillStrategy(_FillStrategy):
    def getUrlParams(self):
        return "fillerK=NoFill"

class _FillLatestStrategy(_FillStrategy):  
    def __init__(self, period):
        self.period = period
    def getUrlParams(self):
        return f"fillerK=LatestValidValue&fillerP={self.period}"

class _FillCustomTimeserieStrategy(_FillStrategy):
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        return f"fillerK=CustomValue&fillerDV={self.val}"   
    

class _FillCustomBidAskStrategy(_FillStrategy):
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        def toQueryParams(vals):
            filtered = filter(lambda x:x[1], vals)
            stringVals = map(lambda x:[x[0], str(x[1])], filtered)
            joinedEqual = map(lambda x:"=".join(x), stringVals)
            return "&".join(joinedEqual)
        return toQueryParams([
            ["fillerK", "CustomValue"],
            ["fillerDVbbp", self.val.get("bestBidPrice")],
            ["fillerDVbap", self.val.get("bestAskPrice")],
            ["fillerDVbbq", self.val.get("bestBidQuantity")],
            ["fillerDVbaq", self.val.get("bestAskQuantity")],
            ["fillerDVlp", self.val.get("lastPrice")],
            ["fillerDVlq", self.val.get("lastQuantity")],
        ])

class _FillCustomMasStrategy(_FillStrategy):
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        def toQueryParams(vals):
            filtered = filter(lambda x:x[1], vals)
            stringVals = map(lambda x:[x[0], str(x[1])], filtered)
            joinedEqual = map(lambda x:"=".join(x), stringVals)
            return "&".join(joinedEqual)
        return toQueryParams([
            ["fillerK", "CustomValue"],
            ["fillerDVs", self.val.get("settlement")],
            ["fillerDVo", self.val.get("open")],
            ["fillerDVc", self.val.get("close")],
            ["fillerDVh", self.val.get("high")],
            ["fillerDVl", self.val.get("low")],
            ["fillerDVvp", self.val.get("volumePaid")],
            ["fillerDVvg", self.val.get("volumeGiven")],
            ["fillerDVvt", self.val.get("volume")],
        ])    
class _QueryParameters: 
    def __init__(self, ids: Optional[List[int]], 
                       extractionRangeConfig: ExtractionRangeConfig = None, 
                       extractionRangeType: ExtractionRangeType = None, 
                       timezone: str = None, 
                       filterId: int = None,
                       fill:_FillStrategy = None) -> None:
                       
        self.ids = ids
        self.extractionRangeConfig = extractionRangeConfig or ExtractionRangeConfig()
        self.extractionRangeType = extractionRangeType
        self.timezone = timezone
        self.filterId = filterId
        self.fill = fill

