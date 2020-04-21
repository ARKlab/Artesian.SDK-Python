from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
import urllib
class _ActualQuery(_Query):
    __routePrefix = "ts"
    def __init__(self, client, requestExecutor, partitionStrategy):
        queryParameters = ActualQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids):
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId):
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz):
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start, end):
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart, pEnd):
        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod):
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval):
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr):
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity):
        self._queryParameters.granularity = granularity
        return self
    def execute(self):
        urls = self.__buildRequest()
        return super()._exec(urls)
    async def executeAsync(self):
        urls = self.__buildRequest()
        return super()._execAsync(urls)
    def __buildRequest(self):
        self.__validateQuery()
        qps = self.__partition.PartitionActual([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{self.__getGranularityPath(qp.granularity)}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids= sep.join(map(str,qp.ids))
                enc = urllib.parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + str(qp.filterId)
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            if not (qp.transformId is None):
                url = url + "&tr=" + str(qp.transformId)
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.granularity is None):
                raise Exception("Extraction granularity must be provided. Use .InGranularity() argument takes a granularity type")
    def __getGranularityPath(self,granularity):
        switcher = {
            Granularity.DAY: "Day",
            Granularity.FIFTEEN_MINUTE: "FifteenMinute",
            Granularity.HOUR: "Hour" ,
            Granularity.MINUTE: "Minute",
            Granularity.MONTH: "Month",
            Granularity.QUARTER: "Quarter",
            Granularity.TEN_MINUTE: "TenMinute",
            Granularity.THIRTY_MINUTE: "ThirtyMinute",
            Granularity.WEEK: "Week",
            Granularity.YEAR: "Year",
        }
        vr = switcher.get(granularity, "VGran")
        if vr == "VGran" :
            raise Exception("Not supported Granularity")
        return vr