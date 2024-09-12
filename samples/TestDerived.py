from Artesian import ArtesianConfig
from Artesian.MarketData import Granularity
from Artesian.Query import QueryService

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)

# AbsoluteRange - TimeZone - MultiIds - MUV
test1 = (
    qs.createDerived()
    .forMarketData([100701091])
    .inAbsoluteDateRange("2018-01-01", "2018-01-02")
    .inTimeZone("UTC")
    .inGranularity(Granularity.Hour)
)

res = test1.forDerived().execute()
