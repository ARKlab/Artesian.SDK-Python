from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.MarketDataType import MarketDataType
from Artesian.MarketData._Enum.UpsertMode import UpsertMode

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

mktId = Artesian.MarketData.MarketDataIdentifier(
    "PythonSDK",
    "TestActualWriteAndDelete"
)

mktDataEntity = Artesian.MarketData.MarketDataEntityInput(
    mktId.provider,
    mktId.name,
    Granularity.Hour,
    MarketDataType.ActualTimeSerie,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(mktId.provider, mktId.name)

if registered is None:
    registered = mkdservice.registerMarketData(mktDataEntity)

data = Artesian.MarketData.UpsertData(
    mktId,
    "UTC",
    rows={datetime(2020, 1, 1, h): 42.0 + h / 24.0 for h in range(0, 23)},
    upsertMode=UpsertMode.Merge
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createActual()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)

# Delete data between 2020-01-01 06:00 and 2020-01-01 18:00
deleteData = Artesian.MarketData.DeleteData(
    mktId,
    timezone="CET",
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
)

mkdservice.deleteData(deleteData)

res = (
    query.createActual()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)


# Delete data between 2020-01-01 06:00 and 2020-01-01 18:00 without Timezone
deleteData = Artesian.MarketData.DeleteData(
    mktId,
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
)

mkdservice.deleteData(deleteData)

res = (
    query.createActual()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)

# Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
