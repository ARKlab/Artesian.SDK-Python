from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Services.Enum.Granularity import Granularity
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
    def withFillNull(self):
        self._queryParameters.fill = NullFillStategy()
        return self
    def withFillNone(self):
        self._queryParameters.fill = NoFillStategy()
        return self
    def withFillLatestValue(self, period):
        self._queryParameters.fill = FillLatestStategy(period)
        return self
    def withFillCustomValue(self, val):
        self._queryParameters.fill = FillCustomStategy(val)
        return self
    def execute(self):
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self):
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
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.granularity is None):
                raise Exception("Extraction granularity must be provided. Use .InGranularity() argument takes a granularity type")
    def __getGranularityPath(self,granularity):
        switcher = {
            Granularity.Day: "Day",
            Granularity.FifteenMinute: "FifteenMinute",
            Granularity.Hour: "Hour" ,
            Granularity.Minute: "Minute",
            Granularity.Month: "Month",
            Granularity.Quarter: "Quarter",
            Granularity.TenMinute: "TenMinute",
            Granularity.ThirtyMinute: "ThirtyMinute",
            Granularity.Week: "Week",
            Granularity.Year: "Year",
        }
        vr = switcher.get(granularity, "VGran")
        if vr == "VGran" :
            raise Exception("Not supported Granularity")
        return vr


class NullFillStategy:
    def getUrlParams(self):
        return "fillerK=Null"

class NoFillStategy:
    def getUrlParams(self):
        return "fillerK=NoFill"

class FillLatestStategy:
    def __init__(self, period):
        self.period = period
    def getUrlParams(self):
        return f"fillerK=LatestValidValue&fillerP={self.period}"

class FillCustomStategy:
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        return f"fillerK=CustomValue&fillerDV={self.val}"        