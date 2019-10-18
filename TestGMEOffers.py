from Artesian import GMEPublicOfferService
from Artesian import ArtesianConfig

cfg = ArtesianConfig("baseaddr","apikey")

qs = GMEPublicOfferService(cfg)

#AbsoluteRange - TimeZone - MultiIds - MUV
test1 = qs.createQuery() \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .forMarket(["MGP"]) \
    .isGroupedBy(["Purpose","Market","FuelType","Unit","Operator"]) \
    .forStatus(["ACC"]) \
    .forUnitType(["UP","UC","UPV","UCV"]) \
    .forZone(["NORD"]) \
    .execute()


res = test1