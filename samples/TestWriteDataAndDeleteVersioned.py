from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.MarketDataType import MarketDataType
from Artesian.MarketData._Enum.UpsertMode import UpsertMode

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

versioned = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestVersionedWriteAndDelete",
    Granularity.Hour,
    MarketDataType.VersionedTimeSerie,
    "UTC",
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
    rows={
        datetime(2020, 1, 1, 0): 11.0,
        datetime(2020, 1, 1, 1): 22.0,
        datetime(2020, 1, 1, 2): 33.0,
        datetime(2020, 1, 1, 3): 44.0,
        datetime(2020, 1, 1, 4): 55.0,
        datetime(2020, 1, 1, 5): 66.0,
        datetime(2020, 1, 1, 6): 77.0,
        datetime(2020, 1, 1, 7): 88.0,
        datetime(2020, 1, 1, 8): 99.0,
        datetime(2020, 1, 1, 9): 100.1,
        datetime(2020, 1, 1, 10): 111.1,
        datetime(2020, 1, 1, 11): 122.1,
        datetime(2020, 1, 1, 12): 133.1,
        datetime(2020, 1, 1, 13): 144.1,
        datetime(2020, 1, 1, 14): 155.1,
        datetime(2020, 1, 1, 15): 166.1,
        datetime(2020, 1, 1, 16): 177.1,
        datetime(2020, 1, 1, 17): 188.1,
        datetime(2020, 1, 1, 18): 199.1,
        datetime(2020, 1, 1, 19): 200.2,
        datetime(2020, 1, 1, 20): 211.2,
        datetime(2020, 1, 1, 21): 222.2,
        datetime(2020, 1, 1, 22): 233.2,
        datetime(2020, 1, 1, 23): 244.2
    },
    upsertMode=UpsertMode.Merge
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
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
    timezone="UTC",
    rangeStart=datetime(2020, 1, 1, 6),
    rangeEnd=datetime(2020, 1, 1, 18),
    version=testVersion,
)

mkdservice.deleteData(deleteData)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
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

data = Artesian.MarketData.UpsertData(
    marketIdentifier,
    "UTC",
    version=testVersion,
    rows={
        datetime(2020, 1, 1, 3): 944.0,
        datetime(2020, 1, 1, 4): 955.0,
        datetime(2020, 1, 1, 5): 966.0,
        datetime(2020, 1, 1, 6): 977.0,
        datetime(2020, 1, 1, 7): 988.0,
        datetime(2020, 1, 1, 8): 999.0,
        datetime(2020, 1, 1, 9): 9100.1,
        datetime(2020, 1, 1, 10): 9111.1,
        datetime(2020, 1, 1, 11): 9122.1,
        datetime(2020, 1, 1, 12): 9133.1,
        datetime(2020, 1, 1, 13): 9144.1,
        datetime(2020, 1, 1, 14): 9155.1,
        datetime(2020, 1, 1, 15): 9166.1,
        datetime(2020, 1, 1, 16): 9177.1,
        datetime(2020, 1, 1, 17): 9188.1,
        datetime(2020, 1, 1, 18): 9199.1,
        datetime(2020, 1, 1, 19): 9200.2,
        datetime(2020, 1, 1, 20): 9211.2,
        datetime(2020, 1, 1, 21): 9222.2,
        datetime(2020, 1, 1, 22): 9233.2,
        datetime(2020, 1, 1, 23): 9244.2
    },
    upsertMode=UpsertMode.Replace
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Hour)
    # .forMUV()
    # .forLastNVersions(2)
    .forVersion("2020-01-01T12:00:00")
    .execute()
)

print(res)

# Delete the curve completely
mkdservice.deleteMarketData(registered.marketDataId)
