from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from dateutil import tz

from Artesian.MarketData._Dto import MarketDataIdentifier
from .._Enum import UpsertMode


@dataclass
class MarketAssessmentValue:
    """
    Class for the Market Assessment Value.

    Attributes:
        settlement: the Market Assessment settlement
        open: the Market Assessment open price
        close: the Market Assessment close price
        high: the Market Assessment high price
        low: the Market Assessment low price
        volumePaid: the Market Assessment volume paid
        volumeGiven: the Market Assessment volume given
        volume: the Market Assessment volume
    """

    settlement: Optional[float] = None
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volumePaid: Optional[float] = None
    volumeGiven: Optional[float] = None
    volume: Optional[float] = None


@dataclass
class BidAskValue:
    """
    Class for the Bid Ask Value.

    Attributes:
        bestBidPrice: the Bid Ask best Bid price
        bestAskPrice: the Bid Ask best Ask price
        bestBidQuantity: the Bid Ask best Bid quantity
        bestAskQuantity: the Bid Ask best Ask quantity
        lastPrice: the Bid Ask last price
        lastQuantity: the Bid Ask last quantity
    """

    bestBidPrice: Optional[float] = None
    bestAskPrice: Optional[float] = None
    bestBidQuantity: Optional[float] = None
    bestAskQuantity: Optional[float] = None
    lastPrice: Optional[float] = None
    lastQuantity: Optional[float] = None


@dataclass
class AuctionBidValue:
    """
    Class for the Auction Bid Value.

    Attributes:
        price: the Auction Bid Value price
        quantity: the Auction Bid Value quantity
    """

    price: float
    quantity: float


@dataclass
class AuctionBids:
    """
    Class for the Auction Bids.

    Attributes:
        bidTimestamp: the Auction Bids timestamp (datetime = ISO format)
        bid: the Auction Bids bid
        offer: the Auction Bids offer
    """

    bidTimestamp: datetime
    bid: List[AuctionBidValue]
    offer: List[AuctionBidValue]


@dataclass
class UpsertData:
    """
    Class for the Upsert Data.

    Attributes:
        ID: the MarketDataIdentifier
        timezone: the Timezone of the rows. Must be the OriginalTimezone
                  when writing Dates or must be ""UTC"" when writing Times
        downloadedAt: the UTC timestamp at which this assessment has been generated
        version: the Version to operate on
        rows: the timeserie data in OriginalTimezone or, when Hourly, must be ""UTC""
        marketAssessment: The Market Data Identifier to upsert. LocalDateTime key is
                          the ReportTime which must be in timezone "timezone")
        bidAsk: the Bid Ask
        auctionRows: the timeserie data in timezone "timezone"
        deferCommandExecution: flag to choose between synchronous
                               and asynchronous command execution
        deferDataGeneration: flag to choose between synchronous
                             and asynchronous data generation (MUV)
        keepNulls: when false, nulls are discarded client side and not sent
        upsertMode: Merge or Replace, when None/Merge then data is merged with existing data
    """

    ID: MarketDataIdentifier
    timezone: str
    downloadedAt: datetime = datetime.utcnow().replace(tzinfo=tz.UTC)
    version: Optional[datetime] = None
    rows: Optional[Dict[datetime, Optional[float]]] = None
    marketAssessment: Optional[Dict[datetime, Dict[str, MarketAssessmentValue]]] = None
    bidAsk: Optional[Dict[datetime, Dict[str, BidAskValue]]] = None
    auctionRows: Optional[Dict[datetime, AuctionBids]] = None
    deferCommandExecution: bool = False
    deferDataGeneration: bool = True
    keepNulls: bool = False
    upsertMode: Optional[UpsertMode] = None
