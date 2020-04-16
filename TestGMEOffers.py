from Artesian import GMEPublicOfferService
from Artesian import ArtesianConfig

cfg = ArtesianConfig("https://test-arkive-proxy-abijnkebhgdtw.azurewebsites.net/ArkTest","NP16E00ikgbfCATUgTxWoE4-3BA2xO8PmQmfMuUqCPuk10PPllxeo9TIX3DCz-xVjM4xazIy-GUYWTICxwQLdenp9dHVqS2DeYBp8e1yd-fhp6yDuAQDul3ElP08ryHs")

qs = GMEPublicOfferService(cfg)


test1 = qs.createQuery() \
    .forDate("2020-04-01") \
    .forMarket(["MGP"]) \
    .forStatus("ACC") \
    .forPurpose("BID") \
    .forZone(["NORD"]) \
    .withPagination(1,10) \
    .execute()


res = test1

suca = ""