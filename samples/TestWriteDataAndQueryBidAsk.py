from datetime import datetime
import Artesian
from Artesian import Query
from dateutil import tz
from Artesian import MarketData
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.UpsertMode import UpsertMode

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

mktId = Artesian.MarketData.MarketDataIdentifier("PythonSDK", "TestBidAskWriteAndRead")

registered = mkdservice.readMarketDataRegistryByName(mktId.provider, mktId.name)

mktDataInput = Artesian.MarketData.MarketDataEntityInput(
    mktId.provider,
    mktId.name,
    Granularity.Hour,
    MarketData.MarketDataType.BidAsk,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]}
)

if registered is None:
    registered = mkdservice.registerMarketData(mktDataInput)

bidAsk = MarketData.UpsertData(
    mktId,
    "UTC",
    bidAsk={
        datetime(2020, 1, 1, 3): {
            "Feb-20": MarketData.BidAskValue(bestBidPrice=15.5, bestAskQuantity=20.3, lastPrice=16.7, lastQuantity=14.1),
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.5, bestAskQuantity=30.4, lastPrice=26.4, lastQuantity=24.3),
        },
        datetime(2020, 1, 1, 6): {
            "Feb-20": MarketData.BidAskValue(bestBidPrice=15.7, bestAskQuantity=20.2, lastPrice=16.6, lastQuantity=14.7),
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.4, bestAskQuantity=30.3, lastPrice=26.8, lastQuantity=24.9),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
    upsertMode=UpsertMode.Merge
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

bidAsk2 = MarketData.UpsertData(
    mktId,
    "UTC",
    bidAsk={
        datetime(2020, 1, 1, 6): {
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.2, bestAskQuantity=20.8, lastPrice=16.4, lastQuantity=24.3),
        },
        datetime(2020, 1, 1, 12): {
            "Mar-20": MarketData.BidAskValue(bestBidPrice=25.1, bestAskQuantity=20.5, lastPrice=16.8, lastQuantity=24.7),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
    upsertMode=UpsertMode.Replace
)

mkdservice.upsertData(bidAsk2)

query2 = Query.QueryService(cfg)

res2 = (
    query2.createBidAsk()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .forProducts(["Feb-20", "Mar-20"])
    .inTimeZone("CET")
    .execute()
)

print(res2)

# Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
