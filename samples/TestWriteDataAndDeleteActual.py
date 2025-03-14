from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

actual = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestActualWriteAndDelete",
    Granularity.Hour,
    MarketDataType.ActualTimeSerie,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(
    actual.providerName, actual.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(actual)

data = Artesian.MarketData.UpsertData(
    Artesian.MarketData.MarketDataIdentifier(
        actual.providerName, actual.marketDataName
    ),
    "UTC",
    rows={datetime(2020, 1, 1, h): 42.0 + h / 24.0 for h in range(0, 23)},
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
    ID=Artesian.MarketData.MarketDataIdentifier(
        registered.providerName, registered.marketDataName
    ),
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
    ID=Artesian.MarketData.MarketDataIdentifier(
        registered.providerName, registered.marketDataName
    ),
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
