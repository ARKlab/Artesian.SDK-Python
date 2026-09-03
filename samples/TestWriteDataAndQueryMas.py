from datetime import datetime
import Artesian
from Artesian import Query
from dateutil import tz
from Artesian import MarketData
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.UpsertMode import UpsertMode

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

mktId = Artesian.MarketData.MarketDataIdentifier("PythonSDK", "TestMasWriteAndRead")

marketDataEntity = Artesian.MarketData.MarketDataEntityInput(
    mktId.provider,
    mktId.name,
    Granularity.Hour,
    MarketData.MarketDataType.MarketAssessment,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(mktId.provider, mktId.name)

if registered is None:
    registered = mkdservice.registerMarketData(marketDataEntity)

marketAssessment = MarketData.UpsertData(
    mktId,
    "UTC",
    marketAssessment={
        datetime(2020, 2, 1, 6): {
            "Mar-20": MarketData.MarketAssessmentValue(open=10.1, close=11.1, settlement=12.1, high=99.9, low=11.1),
            "Apr-20": MarketData.MarketAssessmentValue(open=20.2, close=21.2, settlement=99.9, high=99.9, low=11.1),
        },
        datetime(2020, 2, 1, 12): {
            "Mar-20": MarketData.MarketAssessmentValue(open=11.3, close=12.6, settlement=12.1, high=99.9, low=11.1),
            "Apr-20": MarketData.MarketAssessmentValue(open=21.4, close=22.8, settlement=12.1, high=99.9, low=11.1),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
    upsertMode=UpsertMode.Merge
)

mkdservice.upsertData(marketAssessment)

query = Query.QueryService(cfg)

res = (
    query.createMarketAssessment()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-02-01", "2020-02-02")
    .forProducts(["Mar-20", "Apr-20"])
    .inTimeZone("CET")
    .execute()
)

print(res)

marketAssessment2 = MarketData.UpsertData(
    mktId,
    "UTC",
    marketAssessment={
        datetime(2020, 2, 1, 6): {
            "Apr-20": MarketData.MarketAssessmentValue(open=20.2, close=21.2, settlement=99.9, high=99.9, low=11.1),
        },
        datetime(2020, 2, 1, 12): {
            "Mar-20": MarketData.MarketAssessmentValue(open=11.3, close=12.6, settlement=12.1, high=99.9, low=11.1),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
    upsertMode=UpsertMode.Replace
)

mkdservice.upsertData(marketAssessment2)

query2 = Query.QueryService(cfg)

res2 = (
    query2.createMarketAssessment()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-02-01", "2020-02-02")
    .forProducts(["Mar-20", "Apr-20"])
    .inTimeZone("CET")
    .execute()
)

print(res2)
