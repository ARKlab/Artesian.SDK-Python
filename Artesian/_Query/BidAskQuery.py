from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.BidAskQueryParameters import BidAskQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy

import urllib
class _BidAskQuery(_Query):
    __routePrefix = "ba"
    def __init__(self, client, requestExecutor, partitionStrategy):
        """ Inits _BidAskQuery 
            
            Args:
            
                client credential

                requestExecutor
                
                partitionStrategy. """
        queryParameters = BidAskQueryParameters(None,ExtractionRangeConfig(), None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids):
        """ Select the CURVE ID of interest.

            E.g.: 100000xxx"""
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId):
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz):
        """ Gets the BidAsk Query in a specific TimeZone.

            E.g.: (UTC") / ("CET") / ("EET") / ("WET") / ("Europe/Istanbul") / ("Europe/Moscow")"""
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start, end):
        """ Gets the BidAsk Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            E.g.: ("2021-12-01", "2021-12-31")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart, pEnd):
        """ Gets the BidAsk Query in a relative period range time window.
        
        E.g.: ("P-3D", "P10D") -> from 3 days prior, to be considered until 10 days after."""

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod):
        """ Gets the BidAsk Query in a relative period of a time window.
        
        E.g.: ("P5D")"""
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval):
        """ Gets the Relative Interval considers a specific interval of time window.
        
        E.g.: (RelativeInterval.ROLLING_WEEK) or (RelativeInterval.ROLLING_MONTH)"""
        super()._inRelativeInterval(relativeInterval)
        return self
    def forProducts(self, products):
        """ Gets the Products tor the BidAsk Query in a time window.
        
        E.g.: forProducts(["D+1","Feb-18"])"""
        self._queryParameters.products = products
        return self
    def withFillNull(self):
        """ This is an optional filler strategy for the extraction.
        
        Ex:    withFillNull() """
        self._queryParameters.fill = NullFillStategy()
        return self
    def withFillNone(self):
        """ This is an optional filler strategy for the extraction.
        
        Ex:    withFillNone() """
        self._queryParameters.fill = NoFillStategy()
        return self
    def withFillLatestValue(self, period):
        """ This is an optional filler strategy for the extraction.
        
        Ex:    withFillLatestValue("P5D") """
        self._queryParameters.fill = FillLatestStategy(period)
        return self
    def withFillCustomValue(self, **val):
        """ This is an optional filler strategy for the extraction.
        
        Ex:    //Timeseries
                .withFillCustomValue(123)
               // Market Assessment
                .withFillCustomValue(
                settlement = 123,
                open = 456,
                close = 789,
                high = 321,
                low = 654,
                volumePaid = 987,
                volueGiven = 213,
                volume = 435,
                ) """
        self._queryParameters.fill = FillCustomStategy(val)
        return self
    def execute(self):
        """ Execute the Query."""
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self):
        """ Execute Async Query."""
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
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.products is None):
                raise Exception("Products must be provided for extraction. Use .ForProducts() argument takes a string or string array of products")


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
        def toQueryParams(vals):
            filtered = filter(lambda x:x[1], vals)
            stringVals = map(lambda x:[x[0], str(x[1])], filtered)
            joinedEqual = map(lambda x:"=".join(x), stringVals)
            return "&".join(joinedEqual)
        return toQueryParams([
            ["fillerK", "CustomValue"],
            ["fillerDVbbp", self.val.get("bestBidPrice")],
            ["fillerDVbap", self.val.get("bestAskPrice")],
            ["fillerDVbbq", self.val.get("bestBidQuantity")],
            ["fillerDVbaq", self.val.get("bestAskQuantity")],
            ["fillerDVlp", self.val.get("lastPrice")],
            ["fillerDVlq", self.val.get("lastQuantity")],
        ])
