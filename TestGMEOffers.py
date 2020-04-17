from Artesian import GMEPublicOfferService
from Artesian import ArtesianConfig
from Artesian import Market
from Artesian import Status
from Artesian import Scope
from Artesian import Zone
from Artesian import Purpose

cfg = ArtesianConfig("baseaddr","apikey")

qs = GMEPublicOfferService(cfg)


test1 = qs.createQuery() \
    .forDate("2020-04-01") \
    .forMarket([Market.MGP]) \
    .forStatus(Status.ACC) \
    .forPurpose(Purpose.BID) \
    .forZone([Zone.NORD]) \
    .withPagination(1,10) \
    .execute()


res = test1

