from Artesian import *

cfg = ArtesianConfig("baseaddr","apikey")

qs = QueryService(cfg)

test = qs.createMarketAssessment() \
.forMarketData([100000032,100000043]) \
.forProducts(["D+1","Feb-18"]) \
.inAbsoluteDateRange("2018-01-01","2018-01-02") \
.execute()

print(test)