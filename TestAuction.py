from Artesian import QueryService
from Artesian import ArtesianConfig

cfg = ArtesianConfig("baseaddr","apikey")

qs = QueryService(cfg)

#AbsoluteRange - TimeZone - MultiIds
test1 = qs.createAuction() \
    .forMarketData([100011484,100011472,100011477,100011490,100011468,100011462,100011453]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .execute()
print(test1[1])
#MonoIds 
testR = qs.createAuction() \
    .forMarketData([100011484]) \
    .inTimeZone("UTC") \
#RelatiuvePreriodRange
testPR=testR.inRelativePeriodRange("P0Y0M-1D","P0Y0M1D") \
    .execute()
print(testPR[1])
#InRelativePeriod
testP=testR.inRelativePeriod("P0Y0M-1D") \
    .execute()
print(testP[1])

#Split - Daily
testSplit = qs.createAuction() \
    .forMarketData([100029031,100029044,100011524,100029037,100029033,100029046,100011519,100029042,100063682,100011468,100029032,100029045,100011462,100011538,100029038,100011477,100011554, \
                    100029041,100011580,100011490,100029039,100029040,100011453,100011493,100011516,100011530,100011543,100029043,100011499,100011509,100011549,100029036,100029049,100011458, \
                    100011472,100011562,100029035,100029048,100032778,100011484,100011497,100011507,100011574,100029034,100029047,100032777]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .execute()
print(testSplit[1])

#Filter
testF = qs.createAuction() \
    .forFilterId(1001) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .execute()
print(testF[1])