from Artesian import *
from Artesian.MarketData import MarketDataService

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = MarketDataService(cfg)

res = qs.readCurveRange(100042422, 1, 1000)


res = qs.readCurveRange(
    100042422, 1, 1000, versionFrom="2016-12-20", versionTo="2019-03-12"
)
