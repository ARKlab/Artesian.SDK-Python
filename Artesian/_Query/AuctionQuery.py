from Artesian import _ClientsExecutor
from Artesian._ClientsExecutor import RequestExecutor
from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.AuctionQueryParameters import AuctionQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
import urllib
from typing import List
from __future__ import annotations

class _AuctionQuery(_Query):
    __routePrefix = "auction"
    def __init__(self, client: _ClientsExecutor, requestExecutor: RequestExecutor, partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _AuctionQuery 
         
            Args:
            
                client 

                requestExecutor
                
                partitionStrategy.  """
        queryParameters = AuctionQueryParameters(None,ExtractionRangeConfig(), None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: List[int]) -> _AuctionQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. E.g.: 100000xxx
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _AuctionQuery:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _AuctionQuery:
        """ Gets the Auction Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _AuctionQuery:
        """ Gets the Auction Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: the date start of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
                end:  the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> _AuctionQuery:
        """ Gets the Auction Query in a relative period range time window.
        
            Args:
                pStart: the relative period start of the range of extracted timeseries. (ex. "P--3D")
                pEnd: the relative period end of the range of the extracted timeseries. (ex. "P10D") 
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _AuctionQuery:
        """ Gets the Auction Query in a relative period of a time window.
        
            Args:
                extractionPeriod: the relative period of extracted timeseries. (ex. "P5D")
        """
        super()._inRelativePeriod(extractionPeriod)
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
        qps = self.__partition.PartitionAuction([self._queryParameters])
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
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.ids is None and self._queryParameters.filterId is None):
                raise Exception("Extraction ids or filterid must be provided. Use .forMarketData() or .forFilterId()")