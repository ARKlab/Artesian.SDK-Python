from datetime import datetime
import Artesian
from Artesian import Query
from dateutil import tz
from Artesian import MarketData
from Artesian.Granularity import Granularity

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

marketAssessment = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestMasWriteAndDelete",
    Granularity.Hour,
    MarketData.MarketDataType.MarketAssessment,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(
    marketAssessment.providerName, marketAssessment.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(marketAssessment)

marketAssessment = MarketData.UpsertData(
    Artesian.MarketData.MarketDataIdentifier(
        marketAssessment.providerName, marketAssessment.marketDataName
    ),
    "UTC",
    marketAssessment={
        datetime(2020, 1, 1): {
            "Feb-20": MarketData.MarketAssessmentValue(open=10.0, close=11.0),
            "Mar-20": MarketData.MarketAssessmentValue(open=20.0, close=21.0),
        },
        datetime(2020, 1, 2): {
            "Feb-20": MarketData.MarketAssessmentValue(open=11.0, close=12.0),
            "Mar-20": MarketData.MarketAssessmentValue(open=21.0, close=22.0),
        },
    },
    downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
)

mkdservice.upsertData(marketAssessment)

query = Query.QueryService(cfg)

res = (
    query.createMarketAssessment()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .forProducts(["Feb-20", "Mar-20"])
    .inTimeZone("CET")
    .execute()
)

print(res)

# Delete data with product Feb-20 between 2020-01-01 and 2020-01-03
deleteData = Artesian.MarketData.DeleteData(
    ID=Artesian.MarketData.MarketDataIdentifier(
        registered.providerName, registered.marketDataName
    ),
    timezone="CET",
    rangeStart=datetime(2020, 1, 1, 0),
    rangeEnd=datetime(2020, 1, 3, 0),
    product=["Feb-20"],
)

mkdservice.deleteData(deleteData)

res = (
    query.createMarketAssessment()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .forProducts(["Feb-20", "Mar-20"])
    .inTimeZone("CET")
    .execute()
)

print(res)

# Delete data with product Feb-20 between 2020-01-01 and 2020-01-03 without Timezone
deleteData = Artesian.MarketData.DeleteData(
    ID=Artesian.MarketData.MarketDataIdentifier(
        registered.providerName, registered.marketDataName
    ),
    rangeStart=datetime(2020, 1, 1, 0),
    rangeEnd=datetime(2020, 1, 3, 0),
    product=["Feb-20"],
)

mkdservice.deleteData(deleteData)

res = (
    query.createMarketAssessment()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .forProducts(["Feb-20", "Mar-20"])
    .inTimeZone("CET")
    .execute()
)

print(res)

# Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
