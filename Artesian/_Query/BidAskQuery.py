from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.BidAskQueryParameters import BidAskQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy

import urllib
class _BidAskQuery(_Query):
    __routePrefix = "ba"
    def __init__(self, client, requestExecutor, partitionStrategy):
        queryParameters = BidAskQueryParameters(None,ExtractionRangeConfig(), None, None, None, None) 
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
    def forProducts(self, products):
        self._queryParameters.products = products
        return self
    def execute(self):
        urls = self.__buildRequest()
        return super()._exec(urls)
    async def executeAsync(self):
        urls = self.__buildRequest()
        return super()._execAsync(urls)
    def __buildRequest(self):
        self.__validateQuery()
        qps = self.__partition.PartitionGMEPOffer([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids= sep.join(map(str,qp.ids))
                enc = urllib.parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + str(qp.filterId)
            if not (qp.products is None):
                sep = ","
                prod= enc = urllib.parse.quote_plus(sep.join(qp.products))
                url = url + "&p=" + prod
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.products is None):
                raise Exception("Products must be provided for extraction. Use .ForProducts() argument takes a string or string array of products")