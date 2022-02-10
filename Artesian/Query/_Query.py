from __future__ import annotations
from ._QueryParameters.QueryParameters import _QueryParameters
from ._QueryParameters.ExtractionRangeType import ExtractionRangeType
from .RelativeInterval import RelativeInterval
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client

import asyncio
import itertools
from typing import List

class _Query:
    def __init__(self, client: _Client, 
                       requestExecutor: _RequestExecutor, 
                       queryParameters: _QueryParameters) -> None:
        """ Inits _Query """
            
        self._queryParameters = queryParameters
        self._client = client
        self._requestExecutor = requestExecutor
    def _forMarketData(self, ids: List[int]) -> _Query:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. Ex.: 100000xxx
            
            Returns:
                Query.
        """
        self._queryParameters.ids = ids
        self._queryParameters.filterId = None
        return self
    def _forFilterId(self, filterId: int) -> _Query:
        """ Sets the list of filtered marketdata id to be queried
            
            Args:
                filterId: marketdata filtered by id
            
            Returns:
                Query.
        """
        self._queryParameters.filterId = filterId
        self._queryParameters.ids = None
        return self
    def _inTimezone(self, tz: str) -> _Query:
        """ Gets the Query in a specific TimeZone in IANA format.

            Args:
                tz: "UTC","CET","Europe/Istanbul"
        
             Returns:
                Query.
        """
        self._queryParameters.timezone = tz
        return self
    def _inAbsoluteDateRange(self, start:str, end:str) -> _Query:
        """ Gets the Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
            The Range is end exclusive (ex.: "2022-01-01"->"2022-01-02" extracts a single day)
        
            Args:
                start: string for the date start of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")
                end: string for the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")

            Returns:
                Query.
        """
        self._queryParameters.extractionRangeType = ExtractionRangeType.DateRange
        self._queryParameters.extractionRangeSelectionConfig.dateStart = start
        self._queryParameters.extractionRangeSelectionConfig.dateEnd = end
        return self
    def _inRelativePeriodRange(self, pstart: str, pend: str) -> _Query:
        """ Gets the Query in a relative period range time window.
        
            Args:
                pStart: string for the relative period start of the range of extracted timeseries. (ex.: "P-3D")
                pEnd: string for the relative period end of the range of the extracted timeseries. (ex.: "P10D") 

            Returns:
                Query.
        """

        self._queryParameters.extractionRangeType = ExtractionRangeType.PeriodRange
        self._queryParameters.extractionRangeSelectionConfig.periodFrom = pstart
        self._queryParameters.extractionRangeSelectionConfig.periodTo = pend
        return self
    def _inRelativePeriod(self, period: str) -> _Query:
        """ Gets the Query in a relative period of a time window.
        
            Args:
                extractionPeriod: string for the relative period of extracted timeseries. (ex.: "P5D")

            Returns:
                Query.
        """
        self._queryParameters.extractionRangeType = ExtractionRangeType.Period
        self._queryParameters.extractionRangeSelectionConfig.period = period
        return self
    def _inRelativeInterval(self, relativeInterval: RelativeInterval) -> _Query:
        """ Gets the Relative Interval considers a specific interval of time window.
        
            Args:
                relativeInterval: Enum the relative interval of extracted timeseries. (ex.: "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 

            Returns:
                Query.
        """
        self._queryParameters.extractionRangeType = ExtractionRangeType.RelativeInterval
        self._queryParameters.extractionRangeSelectionConfig.relativeInterval = relativeInterval
        return self
    def _buildExtractionRangeRoute(self, queryParamaters) -> _Query:
        rela = None
        if queryParamaters.extractionRangeSelectionConfig.relativeInterval is not None:
            rela = self.__getRelativeInterval(queryParamaters.extractionRangeSelectionConfig.relativeInterval)
        
        switcher = {
            ExtractionRangeType.DateRange: f"{self.__toUrlParam(queryParamaters.extractionRangeSelectionConfig.dateStart, queryParamaters.extractionRangeSelectionConfig.dateEnd)}",
            ExtractionRangeType.Period: f"{queryParamaters.extractionRangeSelectionConfig.period}",
            ExtractionRangeType.PeriodRange: f"{queryParamaters.extractionRangeSelectionConfig.periodFrom}/{queryParamaters.extractionRangeSelectionConfig.periodTo}",
            ExtractionRangeType.RelativeInterval: f"{rela}"
        }
        subPath = switcher.get(queryParamaters.extractionRangeType, "ExtractionRangeType")
        if subPath == "ExtractionRangeType" or subPath is None :
            raise Exception("Not supported RangeType")
        return subPath
    def _exec(self, urls) -> list:
        loop = get_event_loop()
        rr = loop.run_until_complete(self._execAsync(urls))
        return rr
    async def _execAsync(self, urls) -> list:
            with self._client as c:
                res = await asyncio.gather(*[self._requestExecutor.exec(c.exec, 'GET', i, None) for i in urls])
                return list(itertools.chain(res))
    def __toUrlParam(self, start, end):
        return f"{start}/{end}"
    def _validateQuery(self):
        if(self._queryParameters.extractionRangeType is None):
            raise Exception("Data extraction range must be provided. Provide a date range , period or period range or an interval eg .InAbsoluteDateRange()")
        if(self._queryParameters.ids is None and self._queryParameters.filterId is None):
            raise Exception("Marketadata ids OR filterId must be provided for extraction. Use .ForMarketData() OR .ForFilterId() and provide an integer or integer array as an argument")
    def __getRelativeInterval(self,interval):
        switcher = {
            RelativeInterval.RollingWeek : "RollingWeek",
            RelativeInterval.RollingYear : "RollingYear",
            RelativeInterval.WeekToDate : "WeekToDate",
            RelativeInterval.MonthToDate : "MonthToDate",
            RelativeInterval.QuarterToDate : "QuarterToDate",
            RelativeInterval.RollingMonth : "RollingMonth",
            RelativeInterval.RollingQuarter : "RollingQuarter",
            RelativeInterval.YearToDate : "YearToDate"

        }
        subPath = switcher.get(interval, "RelativeInterval")
        if subPath == "RelativeInterval" :
            raise Exception("Not supported RelativeInterval")
        return subPath


def get_event_loop():
    """
    Wrapper around asyncio get_event_loop.
    Ensures that there is an event loop available.
    An event loop may not be available if the sdk is not run in the main event loop
    """
    try:
        asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    
    return asyncio.get_event_loop()