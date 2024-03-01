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
    "TestAuctionWriteAndDelete",
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

auctionRowData={datetime(2020, 1, 1, h): MarketData.AuctionBids(
            datetime(2020, 1, 1),
            bid=[
                MarketData.AuctionBidValue(11.0, 12.0),
                MarketData.AuctionBidValue(13.0, 14.0),
            ],
            offer=[
                MarketData.AuctionBidValue(21.0, 22.0),
                MarketData.AuctionBidValue(23.0, 24.0),
            ],
        ) for h in range(0, 23)}

auctionRows = MarketData.UpsertData(
    Artesian.MarketData.MarketDataIdentifier(
        auction.providerName, auction.marketDataName
    ),
    "UTC",
    auctionRows=auctionRowData,
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

#Delete data between 2020-01-01 06:00 and 2020-01-01 18:00
deleteData = Artesian.MarketData.DeleteData(
    ID=Artesian.MarketData.MarketDataIdentifier(registered.providerName, registered.marketDataName),
    timezone="CET",
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
)

mkdservice.deleteData(deleteData)

res = (
    query.createAuction()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .execute()
)

print(res)

#Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
