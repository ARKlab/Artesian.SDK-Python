from Artesian import *

cfg = ArtesianConfig("baseaddr","apikey")

qs = GMEPublicOfferService(cfg)


test1 = qs.createQuery() \
    .forDate("2020-04-01") \
    .forMarket([Market.Mgp]) \
    .forStatus(Status.Acc) \
    .forPurpose(Purpose.Bid) \
    .forZone([Zone.Nord]) \
    .withPagination(1,10) \
    .execute()


res = test1

