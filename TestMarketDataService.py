from Artesian import MarketDataService
from Artesian import RelativeInterval
from Artesian import ArtesianConfig

cfg = ArtesianConfig("https://test-arkive-proxy-abijnkebhgdtw.azurewebsites.net/ArkTest","NP16E00ikgbfCATUgTxWoE4-3BA2xO8PmQmfMuUqCPuk10PPllxeo9TIX3DCz-xVjM4xazIy-GUYWTICxwQLdenp9dHVqS2DeYBp8e1yd-fhp6yDuAQDul3ElP08ryHs")

qs = MarketDataService(cfg)

res=qs.readCurveRange(100042422, 1, 1000)


res=qs.readCurveRange(100042422, 1, 1000, versionFrom="2016-12-20" , versionTo="2019-03-12")

