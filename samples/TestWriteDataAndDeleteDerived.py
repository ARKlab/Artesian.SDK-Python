from datetime import datetime
import Artesian
from Artesian import Query
from Artesian import ArtesianConfig
from Artesian.Granularity import Granularity
from Artesian.MarketData._Dto.DerivedCfgCoalesce import DerivedCfgCoalesce
from Artesian.MarketData._Enum import AggregationRule
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

mkdservice = Artesian.MarketData.MarketDataService(cfg)

# Create first versioned curve to use for derived timeseries curve
versioned = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestVersionedC1",
    Granularity.Day,
    MarketDataType.VersionedTimeSerie,
    "UTC",
    # derivedCfg=None,
)

registered = mkdservice.readMarketDataRegistryByName(
    versioned.providerName, versioned.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(versioned)

marketIdentifier = Artesian.MarketData.MarketDataIdentifier(
    versioned.providerName, versioned.marketDataName
)

curveids = []
curveids.append(registered.marketDataId)

testVersion = datetime(2020, 1, 4, 0)

data = Artesian.MarketData.UpsertData(
    marketIdentifier,
    "UTC",
    version=testVersion,
    rows={datetime(2020, 1, d, 0): 100 for d in range(1, 7)},
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-07")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Day)
    .forVersion("2020-01-04T00:00:00")
    .execute()
)

print(res)

# Create second versioned curve to use for derived timeseries curve
versioned = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestVersionedC2",
    Granularity.Day,
    MarketDataType.VersionedTimeSerie,
    "UTC",
)

registered = mkdservice.readMarketDataRegistryByName(
    versioned.providerName, versioned.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(versioned)

marketIdentifier = Artesian.MarketData.MarketDataIdentifier(
    versioned.providerName, versioned.marketDataName
)
curveids.append(registered.marketDataId)
testVersion = datetime(2020, 1, 6, 0)

data = Artesian.MarketData.UpsertData(
    marketIdentifier,
    "UTC",
    version=testVersion,
    rows={datetime(2020, 1, d, 0): 200 for d in range(1, 10)},
)

mkdservice.upsertData(data)

query = Query.QueryService(cfg)

res = (
    query.createVersioned()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-10")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Day)
    .forVersion("2020-01-06T00:00:00")
    .execute()
)

print(res)

# Create deried curve to use from the two versionedtimeseries curves
dCfg = DerivedCfgCoalesce()
dCfg.orderedReferencedMarketDataIds = curveids

derived = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestDerivedNEW",
    Granularity.Day,
    MarketDataType.DerivedTimeSerie,
    "UTC",
    aggregationRule=AggregationRule.AverageAndReplicate,
    derivedCfg=dCfg,
)

registered = mkdservice.readMarketDataRegistryByName(
    derived.providerName, derived.marketDataName
)
if registered is None:
    registered = mkdservice.registerMarketData(derived)

marketIdentifier = Artesian.MarketData.MarketDataIdentifier(
    derived.providerName, derived.marketDataName
)

query = Query.QueryService(cfg)

res = (
    query.createDerived()
    .forMarketData([registered.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-10")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Day)
    .forDerived()
    .execute()
)

print(res)

# Delete the curve completely
# this is currently not working, the request times out on the service side
# mkdservice.deleteMarketData(registered.marketDataId)
