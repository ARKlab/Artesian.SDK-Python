from Artesian import _ClientsExecutor
from Artesian._ClientsExecutor import RequestExecutor
from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
import urllib
from typing import List
from __future__ import annotations

class _ActualQuery(_Query):
    __routePrefix = "ts"
    def __init__(self, client: _ClientsExecutor, requestExecutor: RequestExecutor, partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _ActualQuery
         
            Args:          
                client 

                requestExecutor    

                partitionStrategy. """
        queryParameters = ActualQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: List[int]) -> _ActualQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. E.g.: 100000xxx
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _ActualQuery:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _ActualQuery:
        """ Gets the Actual Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _ActualQuery:
        """ Gets the Actual Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: the date start of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
                end:  the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex. "2022-01-01")
               
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> _ActualQuery:
        """ Gets the Actual Query in a relative period range time window.
        
            Args:
                pStart: the relative period start of the range of extracted timeseries. (ex. "P--3D")
                pEnd: the relative period end of the range of the extracted timeseries. (ex. "P10D") 
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _ActualQuery:
        """ Gets the Actual Query in a relative period of a time window.
        
            Args:
                extractionPeriod: the relative period of extracted timeseries. (ex. "P5D")
                
        """
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: str) -> _ActualQuery:
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: the relative interval of extracted timeseries. (ex. "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 
        """
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr: str) -> _ActualQuery:
        """ Gets the Actual Query in a specific time transform to be queried.

            Args:
                tr: "Custom", "GASDAY66", "THERMALYEAR" .
        """
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity: Granularity) -> _ActualQuery:
        """ Gets the Actual Query in a specific granularity to be queried.
        
            Args:
                granularity: ex.  "TenMinute", "FifteenMinute", "Hour", "Year" 
        """
        self._queryParameters.granularity = granularity
        return self
    def withFillNull(self) -> _ActualQuery:
        """ Optional filler strategy for the extraction.
        
            Args: 
                ex.  withFillNull() 
        """
        self._queryParameters.fill = _NullFillStategy()
        return self
    def withFillNone(self) -> _ActualQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.  withFillNone() 
        """
        self._queryParameters.fill = _NoFillStategy()
        return self
    def withFillLatestValue(self, period: str) -> _ActualQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                ex.    withFillLatestValue("P5D") 
        """
        self._queryParameters.fill = _FillLatestStategy(period)
        return self
    def withFillCustomValue(self, value:float) -> _ActualQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                 ex. 
                //Timeseries
                .withFillCustomValue(123)
        """
        self._queryParameters.fill = _FillCustomStategy(value)
        return self
    def execute(self) -> list:
        """ Execute the Query. """
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self) -> list:
        """ Execute Async Query."""

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
        return f"fillerK=CustomValue&fillerDV={self.val}"        