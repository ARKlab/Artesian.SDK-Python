from Artesian import GMEPublicOfferService
from Artesian import ArtesianConfig

cfg = ArtesianConfig("baseaddr","apikey")

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