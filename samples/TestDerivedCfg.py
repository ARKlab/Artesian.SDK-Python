from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Dto.DerivedCfg import DerivedCfg
from Artesian.MarketData._Enum.DerivedAlgorithm import DerivedAlgorithm
from Artesian.MarketData._Enum.MarketDataType import MarketDataType
import time

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

# curveOne
versionedCurveOne = Artesian.MarketData.MarketDataEntityInput(
    "TestProviderNameDerived",
    "CurveOne",
    Granularity.Hour,
    MarketDataType.VersionedTimeSerie,
    "UTC"
)

registeredCurveOne = mkdservice.readMarketDataRegistryByName(
     versionedCurveOne.providerName, versionedCurveOne.marketDataName
)
if registeredCurveOne is None:
    registeredCurveOne = mkdservice.registerMarketData(versionedCurveOne)

marketIdentifierCurveOne = Artesian.MarketData.MarketDataIdentifier(
    versionedCurveOne.providerName, versionedCurveOne.marketDataName
)

# mkdservice.deleteMarketData(registeredCurveOne.marketDataId)

testVersion = datetime(2020, 1, 1, 12)

data = Artesian.MarketData.UpsertData(
    marketIdentifierCurveOne,
    "UTC",
    version=testVersion,
    rows={datetime(2020, 1, 1, h): h for h in range(0, 8)},
)

mkdservice.upsertData(data)

# curveTwo
versionedCurveTwo = Artesian.MarketData.MarketDataEntityInput(
    "TestProviderNameDerived",
    "CurveTwo",
    Granularity.Hour,
    MarketDataType.VersionedTimeSerie,
    "UTC"
)

registeredCurveTwo = mkdservice.readMarketDataRegistryByName(
    versionedCurveTwo.providerName, versionedCurveTwo.marketDataName
)
if registeredCurveTwo is None:
    registeredCurveTwo = mkdservice.registerMarketData(versionedCurveTwo)

marketIdentifierCurveTwo = Artesian.MarketData.MarketDataIdentifier(
    versionedCurveTwo.providerName, versionedCurveTwo.marketDataName
)

# mkdservice.deleteMarketData(registeredCurveTwo.marketDataId)

testVersion = datetime(2020, 1, 1, 12)

data = Artesian.MarketData.UpsertData(
    marketIdentifierCurveTwo,
    "UTC",
    version=testVersion,
    rows={datetime(2020, 1, 1, h): h*2 for h in range(4, 12)},
)

mkdservice.upsertData(data)

curveIds = [registeredCurveOne.marketDataId, registeredCurveTwo.marketDataId]

# Create DerivedCfgCoalesce with order curveId one and two
derivedCfg = DerivedCfg(
    version=1,
    derivedAlgorithm=DerivedAlgorithm.Coalesce,
    orderedReferencedMarketDataIds=curveIds,
)

actualCurveDerived = Artesian.MarketData.MarketDataEntityInput(
    "TestProviderNameDerived",
    "CurveDerived",
    Granularity.Hour,
    MarketDataType.ActualTimeSerie,
    "UTC",
    derivedCfg=derivedCfg,
)

registeredDerived = mkdservice.readMarketDataRegistryByName(
    actualCurveDerived.providerName, actualCurveDerived.marketDataName
)

# mkdservice.deleteMarketData(registeredDerived.marketDataId)

if registeredDerived is None:
    registeredDerived = mkdservice.registerMarketData(actualCurveDerived)

# check that derivedCfg is as expected
assert (
    registeredDerived.derivedCfg is not None
    and registeredDerived.derivedCfg.derivedAlgorithm == DerivedAlgorithm.Coalesce
), "Derived Algorithm is not the expected (Coalesce)"

marketIdentifierDerived = Artesian.MarketData.MarketDataIdentifier(
    actualCurveDerived.providerName, actualCurveDerived.marketDataName
)

time.sleep(2)

# get the derived curve and check values are in according to the configuration
query = Query.QueryService(cfg)

res = (
    query.createActual()
    .forMarketData([registeredDerived.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)

for i in range(0, 12):
    if i < 8:
        assert res[i]['D'] == i, "Value derived curve is wrong"
    elif i < 12:
        assert res[i]['D'] == (i*2), "Value derived curve is wrong"
    else:
        assert res[i]['D'] == 0

curveIdsUpdate = [registeredCurveTwo.marketDataId, registeredCurveOne.marketDataId]

# Create DerivedCfgCoalesce with order curveId two and one
derivedCfgUpdate = DerivedCfg(
    version=1,
    derivedAlgorithm=DerivedAlgorithm.Coalesce,
    orderedReferencedMarketDataIds=curveIdsUpdate,
)

marketDataUpdated = mkdservice.updateDerivedConfiguration(
                        registeredDerived.marketDataId,
                        derivedCfgUpdate,
                        False)

time.sleep(2)

res = (
    query.createActual()
    .forMarketData([registeredDerived.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)

for i in range(0, 12):
    if i < 4:
        assert res[i]['D'] == i, "Value derived curve is wrong"
    elif i < 12:
        assert res[i]['D'] == (i*2), "Value derived curve is wrong"
    else:
        assert res[i]['D'] == 0

# Delete the curves completely
mkdservice.deleteMarketData(registeredCurveOne.marketDataId)
mkdservice.deleteMarketData(registeredCurveTwo.marketDataId)
mkdservice.deleteMarketData(registeredDerived.marketDataId)
