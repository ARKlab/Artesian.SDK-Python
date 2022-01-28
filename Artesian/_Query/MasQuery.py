from Artesian import _ClientsExecutor
from Artesian._ClientsExecutor import RequestExecutor
from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.MasQueryParameters import MasQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
import urllib
from typing import List
from __future__ import annotations

class _MasQuery(_Query):
    __routePrefix = "mas"
    def __init__(self, client: _ClientsExecutor, requestExecutor: RequestExecutor, partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _MasQuery 
        
        Args:
        
            client 

            requestExecutor 
        
            partitionStrategy. """
        queryParameters = MasQueryParameters(None,ExtractionRangeConfig(), None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: List[int]) -> _MasQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. E.g.: 100000xxx
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _MasQuery:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _MasQuery:
        """ Gets the Mas Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _MasQuery:
        """ Gets the Mas Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: the date start of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
                end:  the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> _MasQuery:
        """ Gets the Mas Query in a relative period range time window.
        
            Args:
                pStart: the relative period start of the range of extracted timeseries. (ex. "P--3D")
                pEnd: the relative period end of the range of the extracted timeseries. (ex. "P10D") 
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _MasQuery:
        """ Gets the Mas Query in a relative period of a time window.
        
            Args:
                extractionPeriod: the relative period of extracted timeseries. (ex. "P5D")
        """
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: str) -> _MasQuery:
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: the relative interval of extracted timeseries. (ex. "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 
        """
        super()._inRelativeInterval(relativeInterval)
        return self
    def forProducts(self, products: str) -> _MasQuery:
        """ Gets the Products tor the BidAsk Query in a time window.
        
            Args:
                forProducts: ["D+1","Feb-18"]"""
        self._queryParameters.products = products
        return self
    def withFillNull(self) -> _MasQuery:
        """ Optional filler strategy for the extraction.
        
            Args: 
                ex.   withFillNull() """
        self._queryParameters.fill = _NullFillStategy()
        return self
    def withFillNone(self) -> _MasQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.   withFillNone() """
        self._queryParameters.fill = _NoFillStategy()
        return self
    def withFillLatestValue(self, period: str) -> _MasQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.   withFillLatestValue("P5D") """
        self._queryParameters.fill = _FillLatestStategy(period)
        return self
    def withFillCustomValue(self, **val) -> _MasQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex. 
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
        self._queryParameters.fill = _FillCustomStategy(val)
        return self
    def execute(self) -> list:
        """ Execute the Query."""
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self) -> list:
        """ Execute Async Query."""
        urls = self.__buildRequest()
        return super()._execAsync(urls)
    def __buildRequest(self):
        self.__validateQuery()
        qps = self.__partition.PartitionMas([self._queryParameters])
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


class _NullFillStategy:
    def getUrlParams(self):
        return "fillerK=Null"

class _NoFillStategy:    
    def getUrlParams(self):
        return "fillerK=NoFill"

class _FillLatestStategy:    
    def __init__(self, period):
        self.period = period
    def getUrlParams(self):
        return f"fillerK=LatestValidValue&fillerP={self.period}"

class _FillCustomStategy:
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
            ["fillerDVs", self.val.get("settlement")],
            ["fillerDVo", self.val.get("open")],
            ["fillerDVc", self.val.get("close")],
            ["fillerDVh", self.val.get("high")],
            ["fillerDVl", self.val.get("low")],
            ["fillerDVvp", self.val.get("volumePaid")],
            ["fillerDVvg", self.val.get("volueGiven")],
            ["fillerDVvt", self.val.get("volume")],
        ])                