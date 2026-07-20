from enum import Enum


class MarketDataTypeV2(Enum):
    ActualTimeSerie = 0
    VersionedTimeSerie = 1
    MarketAssessment = 2
    Auction = 3
    BidAsk = 4
