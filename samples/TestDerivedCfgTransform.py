from datetime import datetime
import Artesian
from Artesian.Granularity import Granularity
from Artesian.MarketData._Dto.DerivedCfg import DerivedCfg
from Artesian.MarketData._Enum.DerivedAlgorithm import DerivedAlgorithm
from Artesian.MarketData._Enum.MarketDataTypeV2 import MarketDataTypeV2
import time

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

mkdservice = Artesian.MarketData.MarketDataService(cfg)

# curveOne
actualCurveOne = Artesian.MarketData.MarketDataEntityInput(
    "TestProviderNameDerivedTransform",
    "CurveOne",
    Granularity.Hour,
    MarketDataTypeV2.ActualTimeSerie,
    "UTC"
)

registeredCurveOne = mkdservice.readMarketDataRegistryByName(
     actualCurveOne.providerName, actualCurveOne.marketDataName
)
if registeredCurveOne is None:
    registeredCurveOne = mkdservice.registerMarketData(actualCurveOne)

marketIdentifierCurveOne = Artesian.MarketData.MarketDataIdentifier(
    actualCurveOne.providerName, actualCurveOne.marketDataName
)

# mkdservice.deleteMarketData(registeredCurveOne.marketDataId)

data = Artesian.MarketData.UpsertData(
    marketIdentifierCurveOne,
    "UTC",
    rows={datetime(2020, 1, 1, h): 10 for h in range(0, 8)},
)

mkdservice.upsertData(data)

curveIds = [registeredCurveOne.marketDataId]

# Create DerivedCfgTransform
derivedCfg = DerivedCfg(
    version=1,
    derivedAlgorithm=DerivedAlgorithm.Transform,
    transform="SELECT Time, (Value + 1) as Value FROM $table",
    orderedReferencedMarketDataIds=curveIds,
)

actualCurveDerived = Artesian.MarketData.MarketDataEntityInput(
    "TestProviderNameDerivedTransform",
    "CurveDerived",
    Granularity.Hour,
    MarketDataTypeV2.ActualTimeSerie,
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
    and registeredDerived.derivedCfg.derivedAlgorithm == DerivedAlgorithm.Transform
), "Derived Algorithm is not the expected (Transform)"

marketIdentifierDerived = Artesian.MarketData.MarketDataIdentifier(
    actualCurveDerived.providerName, actualCurveDerived.marketDataName
)

time.sleep(2)

# get the derived curve and check values are in according to the configuration
query = Artesian.Query.QueryService(cfg)

res = (
    query.createActual()
    .forMarketData([registeredDerived.marketDataId])
    .inAbsoluteDateRange("2020-01-01", "2020-01-02")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Hour)
    .execute()
)

print(res)

for i in range(0, 8):
    assert res[i]['D'] == 11

# Delete the curves completely
mkdservice.deleteMarketData(registeredCurveOne.marketDataId)
mkdservice.deleteMarketData(registeredDerived.marketDataId)
