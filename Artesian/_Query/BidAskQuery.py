from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.BidAskQueryParameters import BidAskQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from typing import List
from __future__ import annotations

import urllib
class _BidAskQuery(_Query):
    __routePrefix = "ba"
    def __init__(self, client: _Client, requestExecutor: _RequestExecutor, partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _BidAskQuery 
            
            Args:
            
                client

                requestExecutor
                
                partitionStrategy. """
        queryParameters = BidAskQueryParameters(None,ExtractionRangeConfig(), None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: List[int]) -> _BidAskQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. E.g.: 100000xxx
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _BidAskQuery:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _BidAskQuery:
        """ Gets the BidAsk Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _BidAskQuery:
        """ Gets the BidAsk Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: the date start of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
                end:  the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> _BidAskQuery:
        """ Gets the BidAsk Query in a relative period range time window.
        
            Args:
                pStart: the relative period start of the range of extracted timeseries. (ex. "P--3D")
                pEnd: the relative period end of the range of the extracted timeseries. (ex. "P10D") 
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _BidAskQuery:
        """ Gets the BidAsk Query in a relative period of a time window.
        
            Args:
                extractionPeriod: the relative period of extracted timeseries. (ex. "P5D")
        """
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: str) -> _BidAskQuery:
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: the relative interval of extracted timeseries. (ex. "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 
        """
        super()._inRelativeInterval(relativeInterval)
        return self
    def forProducts(self, products: str) -> _BidAskQuery:
        """ Gets the Products tor the BidAsk Query in a time window.
        
            Args:
                forProducts: ["D+1","Feb-18"]"""
        self._queryParameters.products = products
        return self
    def withFillNull(self) -> _BidAskQuery:
        """ Optional filler strategy for the extraction.
        
            Args: 
                ex.  withFillNull() """
        self._queryParameters.fill = _NullFillStategy()
        return self
    def withFillNone(self) -> _BidAskQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.  withFillNone() """
        self._queryParameters.fill = _NoFillStategy()
        return self
    def withFillLatestValue(self, period: str) -> _BidAskQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
               period:  ex.  withFillLatestValue("P5D") """
        self._queryParameters.fill = _FillLatestStategy(period)
        return self
    def withFillCustomValue(self, **val) -> _BidAskQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex. 
                //Timeseries
                .withFillCustomValue(123)
         """
        self._queryParameters.fill = _FillCustomStategy(val)
        return self
    def execute(self) -> list:
        """ Execute the Query."""
        urls = self.__buildRequest()
        return super()._exec(urls)
    async def executeAsync(self) -> list:
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
            ["fillerDVbbp", self.val.get("bestBidPrice")],
            ["fillerDVbap", self.val.get("bestAskPrice")],
            ["fillerDVbbq", self.val.get("bestBidQuantity")],
            ["fillerDVbaq", self.val.get("bestAskQuantity")],
            ["fillerDVlp", self.val.get("lastPrice")],
            ["fillerDVlq", self.val.get("lastQuantity")],
        ])
