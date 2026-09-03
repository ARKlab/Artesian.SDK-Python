from datetime import datetime
import Artesian
from Artesian import Query
from dateutil import tz
from Artesian import MarketData
from Artesian.Granularity import Granularity

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

auction = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestAuctionWriteAndRead",
    Granularity.Hour,
    MarketData.MarketDataType.Auction,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(
    auction.providerName, auction.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(auction)

auctionRows = MarketData.UpsertData(
    Artesian.MarketData.MarketDataIdentifier(
        auction.providerName, auction.marketDataName
    ),
    "UTC",
    auctionRows={
        datetime(2020, 1, 1): MarketData.AuctionBids(
            datetime(2020, 1, 1),
            bid=[
                MarketData.AuctionBidValue(11.0, 12.0),
                MarketData.AuctionBidValue(13.0, 14.0),
            ],
            offer=[
                MarketData.AuctionBidValue(21.0, 22.0),
                MarketData.AuctionBidValue(23.0, 24.0),
            ],
        )
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
)

mkdservice.upsertData(auctionRows)

query = Query.QueryService(cfg)

res = (
    query.createAuction()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .execute()
)

print(res)
