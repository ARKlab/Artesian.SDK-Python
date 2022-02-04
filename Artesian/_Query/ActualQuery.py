
from __future__ import annotations

from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Services.Enum.Granularity import Granularity
import urllib
from typing import List

from Artesian._Services.Enum.RelativeInterval import RelativeInterval

class _ActualQuery(_Query):
    __routePrefix = "ts"
    def __init__(self, client: _Client, 
                       requestExecutor: _RequestExecutor, 
                       partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _ActualQuery """

        queryParameters = ActualQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None) 
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self.__partition= partitionStrategy

    def forMarketData(self, ids: List[int]) -> _ActualQuery:
        """ 
            Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. Ex.: 100000xxx

            Returns: 
                ActualQuery.
        """
        super()._forMarketData(ids)
        return self
    def forFilterId(self, filterId: int) -> _ActualQuery:
        """ 
            Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: marketdata filtered by id to be queried.

            Returns: 
                ActualQuery.
        """
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz: str) -> _ActualQuery:
        """ 
            Gets the Actual Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
            
            Returns: 
                ActualQuery.
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start: str, end: str) -> _ActualQuery:
        """ 
            Gets the Actual Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start: string for the date start of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")
                
                end: string for the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")

            Returns: 
                ActualQuery.       
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> _ActualQuery:
        """ 
            Gets the Actual Query in a relative period range time window.
        
            Args:
                pStart: string for the relative period start of the range of extracted timeseries. (ex.: "P-3D")
                
                pEnd: string for the relative period end of the range of the extracted timeseries. (ex.: "P10D") 
            
            Returns: 
                ActualQuery.
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str) -> _ActualQuery:
        """ 
            Gets the Actual Query in a relative period of a time window.
        
            Args:
                extractionPeriod: string for the relative period of extracted timeseries. (ex.: "P5D")

           Returns: 
                ActualQuery.     
        """
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: RelativeInterval) -> _ActualQuery:
        """ 
            Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: Enum for the relative interval of extracted timeseries. (ex.: "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 

            Returns: 
                ActualQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr: str) -> _ActualQuery:
        """ 
            Gets the Actual Query in a specific time transform to be queried.

            Args:
                tr: "Custom", "GASDAY66", "THERMALYEAR" 
            
            Returns: 
                ActualQuery.
        """
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity: Granularity) -> _ActualQuery:
        """ 
            Gets the Actual Query in a specific granularity to be queried.
        
            Args:
                granularity: Enum ex.: "TenMinute", "FifteenMinute", "Hour", "Year" 

            Returns: 
                ActualQuery.
        """
        self._queryParameters.granularity = granularity
        return self
    def withFillNull(self) -> _ActualQuery:
        """ 
            Optional filler strategy for the extraction.
         
                ex.: withFillNull() 

            Returns: 
                ActualQuery.
        """
        self._queryParameters.fill = _NullFillStategy()
        return self
    def withFillNone(self) -> _ActualQuery:
        """ 
            Optional filler strategy for the extraction.
        
                ex.: withFillNone() 

            Returns: 
                ActualQuery.
        """
        self._queryParameters.fill = _NoFillStategy()
        return self
    def withFillLatestValue(self, period: str) -> _ActualQuery:
        """ 
            Optional filler strategy for the extraction.
        
            Args:
                period: string of the last period value to fill in case there are missing values. Ex.: withFillLatestValue("P5D") 
            
            Returns: 
                ActualQuery.
        """
        self._queryParameters.fill = _FillLatestStategy(period)
        return self
    def withFillCustomValue(self, value:float) -> _ActualQuery:
        """ 
            Optional filler strategy for the extraction.
        
            Args:
                value: float value to fill in case there are missing values. Ex.:  .withFillCustomValue(10)
            
            Returns: 
                ActualQuery.
        """
        self._queryParameters.fill = _FillCustomStategy(value)
        return self
    def execute(self) -> list:
        """ 
            Execute the Query. 
        
            Returns:
                list of ActualQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self) -> list:
        """ 
            Execute Async Query.
            
            Returns:
                list of ActualQuery."""
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