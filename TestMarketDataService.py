from Services.MarketDataService import MarketDataService
from Query.Config.RelativeInterval import RelativeInterval
from Configuration.ArtesianConfig import ArtesianConfig
cfg = ArtesianConfig("baseaddr","apikey")

qs = MarketDataService(cfg)

res=qs.readCurveRange(100042422, 1, 1000)


res=qs.readCurveRange(100042422, 1, 1000, versionFrom="2016-12-20" , versionTo="2019-03-12")

