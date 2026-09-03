from datetime import datetime
import Artesian
from Artesian import Query
from Artesian.Granularity import Granularity
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

actual = Artesian.MarketData.MarketDataEntityInput(
    "PythonSDK",
    "TestActualWriteAndRead",
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
