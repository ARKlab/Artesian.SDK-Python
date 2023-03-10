from datetime import datetime
import Artesian
from Artesian import Query
from dateutil import tz
from Artesian import MarketData
from Artesian.Granularity import Granularity

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

bidAsk = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestBidAskWriteAndRead",
    Granularity.Hour,
    MarketData.MarketDataType.BidAsk,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(
    bidAsk.providerName, bidAsk.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(bidAsk)

bidAsk = MarketData.UpsertData(
    Artesian.MarketData.MarketDataIdentifier(
        bidAsk.providerName, bidAsk.marketDataName
    ),
    "UTC",
    bidAsk={
        datetime(2020, 1, 1): {
            "Feb-20": MarketData.BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.0, lastQuantity=24.0),
        },
        datetime(2020, 1, 2): {
            "Feb-20": MarketData.BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.0, lastQuantity=24.0),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
)

mkdservice.upsertData(bidAsk)

query = Query.QueryService(cfg)

res = (
    query.createBidAsk()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .forProducts(["Feb-20", "Mar-20"])
    .inTimeZone("CET")
    .execute()
)

print(res)
