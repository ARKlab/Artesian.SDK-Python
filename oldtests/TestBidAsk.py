from Artesian import *

cfg = ArtesianConfig("baseaddr","apikey")

qs = QueryService(cfg)

test = qs.createBidAsk() \
.forMarketData([100219392]) \
.forProducts(["D+1","Feb-18"]) \
.inAbsoluteDateRange("2018-01-01","2018-01-02") \
.execute()

print(test)
