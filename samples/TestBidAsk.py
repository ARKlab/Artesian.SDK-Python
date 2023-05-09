from Artesian import *

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = Query.QueryService(cfg)

test = (
    qs.createBidAsk()
    .forMarketData([100219392])
    .forProducts(["D+1", "Feb-18"])
    .inAbsoluteDateRange("2018-01-01", "2018-01-02")
    .execute()
)

print(test)
