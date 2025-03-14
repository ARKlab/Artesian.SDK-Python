from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

versioned = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestVersionedWriteAndDelete",
    Granularity.Hour,
    MarketDataType.VersionedTimeSerie,
    "CET",
    tags={"TestSDKPython": ["PythonValue2"]},
)

registered = mkdservice.readMarketDataRegistryByName(
    versioned.providerName, versioned.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(versioned)

marketIdentifier = Artesian.MarketData.MarketDataIdentifier(
    versioned.providerName, versioned.marketDataName
)
testVersion = datetime(2020, 1, 1, 12)

data = Artesian.MarketData.UpsertData(
    marketIdentifier,
    "UTC",
    version=testVersion,
    rows={datetime(2020, 1, 1, h): 42.0 + h / 24.0 for h in range(0, 23)},
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    # .forMUV()
    # .forLastNVersions(2)
    .forVersion("2020-01-01T12:00:00")
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
    version=testVersion,
)

mkdservice.deleteData(deleteData)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    .forVersion("2020-01-01T12:00:00")
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
    version=testVersion,
)

mkdservice.deleteData(deleteData)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("CET")
    .inGranularity(Granularity.Hour)
    .forVersion("2020-01-01T12:00:00")
    .execute()
)

print(res)

# Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
