from Artesian import MarketDataService
from Artesian import RelativeInterval
from Artesian import ArtesianConfig

cfg = ArtesianConfig("baseaddr","apikey")

qs = MarketDataService(cfg)

res=qs.readCurveRange(100042422, 1, 1000)


res=qs.readCurveRange(100042422, 1, 1000, versionFrom="2016-12-20" , versionTo="2019-03-12")

