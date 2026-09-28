from dataclasses import dataclass, field
from datetime import datetime

from dateutil import tz

from Artesian._ClientsExecutor.ArtesianJsonSerializer import keyValueArrayField

from .._Enum import UpsertMode
from .MarketDataIdentifier import MarketDataIdentifier


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

    settlement: float | None = None
    open: float | None = None
    close: float | None = None
    high: float | None = None
    low: float | None = None
    volumePaid: float | None = None
    volumeGiven: float | None = None
    volume: float | None = None


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

    bestBidPrice: float | None = None
    bestAskPrice: float | None = None
    bestBidQuantity: float | None = None
    bestAskQuantity: float | None = None
    lastPrice: float | None = None
    lastQuantity: float | None = None


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
    bid: list[AuctionBidValue]
    offer: list[AuctionBidValue]


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
    downloadedAt: datetime = field(default_factory=lambda: datetime.now(tz.UTC))
    version: datetime | None = None
    rows: dict[datetime, float | None] | None = keyValueArrayField()
    marketAssessment: dict[datetime, dict[str, MarketAssessmentValue]] | None = keyValueArrayField()
    bidAsk: dict[datetime, dict[str, BidAskValue]] | None = keyValueArrayField()
    auctionRows: dict[datetime, AuctionBids] | None = keyValueArrayField()
    deferCommandExecution: bool = False
    deferDataGeneration: bool = True
    keepNulls: bool = False
    upsertMode: UpsertMode | None = None
