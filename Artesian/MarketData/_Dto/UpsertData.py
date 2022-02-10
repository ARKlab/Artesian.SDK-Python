from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from Artesian.MarketData._Dto import MarketDataIdentifier

@dataclass
class MarketAssessmentValue:
    settlement:Optional[float]=None
    open:Optional[float]=None
    close:Optional[float]=None
    high:Optional[float]=None
    low:Optional[float]=None
    volumePaid:Optional[float]=None
    volumeGiven:Optional[float]=None
    volume:Optional[float]=None

@dataclass
class BidAskValue:
    bestBidPrice:Optional[float]=None
    bestAskPrice:Optional[float]=None
    bestBidQuantity:Optional[float]=None
    bestAskQuantity:Optional[float]=None
    lastPrice:Optional[float]=None
    lastQuantity:Optional[float]=None

@dataclass
class AuctionBidValue:
    price:float
    quantity:float

@dataclass
class AuctionBids:
    bidTimestamp:datetime
    bid:List[AuctionBidValue]=None
    offer:List[AuctionBidValue]=None


@dataclass
class UpsertData:
    ID:MarketDataIdentifier
    timezone:str
    downloadedAt:datetime=datetime.utcnow()
    version:Optional[datetime]=None
    rows:Optional[Dict[datetime, Optional[float]]]=None
    marketAssessment:Optional[Dict[datetime,Dict[str, MarketAssessmentValue]]]=None
    bidAsk:Optional[Dict[datetime,Dict[str, BidAskValue]]]=None
    auctionRows:Optional[Dict[datetime, AuctionBids]]=None
    deferCommandExecution:bool=True
    deferDataGeneration:bool=True
    keepNulls:bool=False
