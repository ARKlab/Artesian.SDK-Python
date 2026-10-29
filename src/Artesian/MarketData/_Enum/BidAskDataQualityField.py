from enum import Enum


class BidAskDataQualityField(Enum):
    Unspecified = 0
    BestBidPrice = 1
    BestAskPrice = 2
    BestBidQuantity = 3
    BestAskQuantity = 4
    LastPrice = 5
    LastQuantity = 6
