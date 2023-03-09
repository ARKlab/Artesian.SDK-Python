from Artesian import ArtesianConfig
from Artesian.Query import QueryService

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)

# AbsoluteRange - TimeZone - MultiIds
test1 = (
    qs.createAuction()
    .forMarketData([100181960, 100181959, 100181958, 100181956])
    .inAbsoluteDateRange("2020-04-01", "2020-04-02")
    .inTimeZone("CET")
    .execute()
)
print(test1[1])
# MonoIds
testR = qs.createAuction().forMarketData([100181960]).inTimeZone("UTC")
# RelatiuvePreriodRange
testPR = testR.inRelativePeriodRange("P0Y0M-10D", "P0Y0M1D").execute()
print(testPR[1])
# InRelativePeriod
testP = testR.inRelativePeriod("P0Y0M-10D").execute()
print(testP[1])

# Split - Daily
testSplit = (
    qs.createAuction()
    .forMarketData(
        [
            100181943,
            100181945,
            100181946,
            100181947,
            100181949,
            100181950,
            100181951,
            100181952,
            100181954,
            100181955,
            100181956,
            100181957,
            100181958,
            100181959,
            100181960,
            100181961,
            100181962,
            100181963,
            100181964,
            100181966,
            100181967,
            100181969,
            100181970,
            100181971,
            100181972,
            100181973,
            100181975,
            100181976,
            100181977,
            100181978,
            100181979,
            100181980,
            100181981,
            100181983,
            100181984,
            100181986,
            100181987,
            100181988,
            100181989,
            100181990,
            100181992,
            100181993,
            100181994,
            100181995,
            100181996,
            100181997,
            100181998,
            100181999,
            100182000,
        ]
    )
    .inAbsoluteDateRange("2020-04-01", "2020-04-02")
    .inTimeZone("UTC")
    .execute()
)
print(testSplit[1])

# Filter
testF = (
    qs.createAuction()
    .forFilterId(1048)
    .inAbsoluteDateRange("2020-04-01", "2020-04-02")
    .inTimeZone("UTC")
    .execute()
)
print(testF[1])
