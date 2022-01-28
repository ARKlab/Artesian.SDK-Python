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
    def __init__(self, client: _ClientsExecutor, requestExecutor: RequestExecutor, partitionStrategy: DefaultPartitionStrategy):
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
    def forFilterId(self, filterId: int):
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: list of marketdata filtered by id"""
        super()._forFilterId(filterId)
        return self
    def inTimeZone(self, tz):
        """ Gets the Actual Query in a specific TimeZone in IANA format.

            Args:
                timezone: "UTC","CET","Europe/Istanbul"
        """
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start, end):
        """ Gets the Actual Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            Args:
                start, end: ("2021-12-01", "2021-12-31")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart, pEnd):
        """ Gets the Actual Query in a relative period range time window.
        
            Args:
                pStart, pEnd: ("P-3D", "P10D")"""

        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod: str):
        """ Gets the Actual Query in a relative period of a time window.
        
            Args:
                extractionPeriod: ("P5D")"""
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval: str):
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: ""RelativeInterval.ROLLING_WEEK"" or "RelativeInterval.ROLLING_MONTH"."""
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr: str):
        """Gets the Actual Query in a specific time transform to be queried.

            Args:
                timetransform:  "Custom", "GASDAY66", "THERMALYEAR" ."""
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity: Granularity):
        """ Gets the Actual Query in a specific granularity to be queried.
        
            Args:
                granularity: e.g.: "TenMinute", "FifteenMinute", "Hour", "Year" """
        self._queryParameters.granularity = granularity
        return self
    def withFillNull(self):
        """ Optional filler strategy for the extraction.
        
            Args: 
                e.g.: withFillNull() """
        self._queryParameters.fill = NullFillStategy()
        return self
    def withFillNone(self):
        """ Optional filler strategy for the extraction.
        
            Args:
                e.g.: withFillNone() """
        self._queryParameters.fill = NoFillStategy()
        return self
    def withFillLatestValue(self, period):
        """ Optional filler strategy for the extraction.
        
            Args:
               e.g.:   withFillLatestValue("P5D") """
        self._queryParameters.fill = FillLatestStategy(period)
        return self
    def withFillCustomValue(self, value:float) -> _ActualQuery:
        """ Optional filler strategy for the extraction.
        
            Args:
                value: value used to fill the missing timeserie points
        """
        self._queryParameters.fill = FillCustomStategy(value)
        return self
    def execute(self):
        """ Execute the Query. """
        urls = self.__buildRequest()
        return super()._exec(urls)
    def executeAsync(self):
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

class NullFillStategy:
    """ Class that sets the Null Filling Strategy."""
    def getUrlParams(self):
        return "fillerK=Null"

class NoFillStategy:
    """ Class that sets the No Filling Strategy."""
    
    def getUrlParams(self):
        return "fillerK=NoFill"

class FillLatestStategy:
    """ Class that sets the Last Filling Strategy."""
   
    def __init__(self, period):
        self.period = period
    def getUrlParams(self):
        return f"fillerK=LatestValidValue&fillerP={self.period}"

class FillCustomStategy:
    """Class that sets the Custom Filling Strategy."""
    def __init__(self, val):
        self.val = val
    def getUrlParams(self):
        return f"fillerK=CustomValue&fillerDV={self.val}"        