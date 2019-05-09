from Services.QueryService import QueryService
from Query.Config.Granularity import Granularity
from Query.Config.RelativeInterval import RelativeInterval
from Configuration.ArtesianConfig import ArtesianConfig

cfg = ArtesianConfig("baseaddr","apikey")

qs = QueryService(cfg)

#AbsoluteRange - TimeZone - MultiIds - MUV
test1 = qs.createVersioned() \
    .forMarketData([100042422,100042283,100042285,100042281,100042287,100042291,100042289]) \
    .inAbsoluteDateRange("2018-01-01","2018-01-02") \
    .inTimeZone("UTC") \
    .inGranularity(Granularity.HOUR)


test1.forMUV().execute()
test1.forLastNVersions(2).execute()
test1.forLastOfDays("2019-03-12","2019-03-16").execute()
test1.forLastOfDays("P0Y0M-2D","P0Y0M2D").execute()
test1.forLastOfDays("P0Y0M-2D").execute()
test1.forLastOfMonths("2019-03-12","2019-03-16").execute()
test1.forLastOfMonths("P0Y-1M0D","P0Y1M0D").execute()
test1.forLastOfMonths("P0Y-1M0D").execute()
test1.forVersion("2019-03-12T14:30:00").execute()