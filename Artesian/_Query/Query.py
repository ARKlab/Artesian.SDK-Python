from Artesian._Query.Config.ExtractionRangeType import ExtractionRangeType
from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
from Artesian._Query.Config.RelativeInterval import RelativeInterval
import asyncio
import itertools
class _Query:
    def __init__(self, client, requestExecutor, queryParameters):
        """ Inits _Query 
        
        Args:
            client credential

            requestExecutor

            partitionStrategy. """
            
        self._queryParameters = queryParameters
        self._client = client
        self._requestExecutor = requestExecutor
    def _forMarketData(self, ids):
        """ Select the CURVE ID of interest.

            E.g.: 100000xxx"""
        self._queryParameters.ids = ids
        self._queryParameters.filterId = None
        return self
    def _forFilterId(self, filterId):
        self._queryParameters.filterId = filterId
        self._queryParameters.ids = None
        return self
    def _inTimezone(self, tz):
        """ Gets the Query in a specific TimeZone.

            E.g.: (UTC") / ("CET") / ("EET") / ("WET") / ("Europe/Istanbul") / ("Europe/Moscow")"""
        self._queryParameters.timezone = tz
        return self
    def _inAbsoluteDateRange(self, start, end):
        """ Gets the Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            E.g.: ("2021-12-01", "2021-12-31")
        """
        self._queryParameters.extractionRangeType = ExtractionRangeType.DATE_RANGE
        self._queryParameters.extractionRangeSelectionConfig.dateStart = start
        self._queryParameters.extractionRangeSelectionConfig.dateEnd = end
        return self
    def _inRelativePeriodRange(self, pstart, pend):
        """ Gets the Query in a relative period range time window.
        
        E.g.: ("P-3D", "P10D") -> from 3 days prior, to be considered until 10 days after."""


        self._queryParameters.extractionRangeType = ExtractionRangeType.PERIOD_RANGE
        self._queryParameters.extractionRangeSelectionConfig.periodFrom = pstart
        self._queryParameters.extractionRangeSelectionConfig.periodTo = pend
        return self
    def _inRelativePeriod(self, period):
        """ Gets the Query in a relative period of a time window.
        
            E.g.: ("P5D")"""
        self._queryParameters.extractionRangeType = ExtractionRangeType.PERIOD
        self._queryParameters.extractionRangeSelectionConfig.period = period
        return self
    def _inRelativeInterval(self, relativeInterval):
        """ The Relative Interval considers a specific interval of time.
        
        E.g.: (RelativeInterval.ROLLING_WEEK) or (RelativeInterval.ROLLING_MONTH)"""
        self._queryParameters.extractionRangeType = ExtractionRangeType.RELATIVE_INTERVAL
        self._queryParameters.extractionRangeSelectionConfig.relativeInterval = relativeInterval
        return self
    def _buildExtractionRangeRoute(self, queryParamaters):
        rela = None
        if queryParamaters.extractionRangeSelectionConfig.relativeInterval is not None:
            rela = self.__getRelativeInterval(queryParamaters.extractionRangeSelectionConfig.relativeInterval)
        
        switcher = {
            ExtractionRangeType.DATE_RANGE: f"{self.__toUrlParam(queryParamaters.extractionRangeSelectionConfig.dateStart, queryParamaters.extractionRangeSelectionConfig.dateEnd)}",
            ExtractionRangeType.PERIOD: f"{queryParamaters.extractionRangeSelectionConfig.period}",
            ExtractionRangeType.PERIOD_RANGE: f"{queryParamaters.extractionRangeSelectionConfig.periodFrom}/{queryParamaters.extractionRangeSelectionConfig.periodTo}",
            ExtractionRangeType.RELATIVE_INTERVAL: f"{rela}"
        }
        subPath = switcher.get(queryParamaters.extractionRangeType, "ExtractionRangeType")
        if subPath == "ExtractionRangeType" or subPath is None :
            raise Exception("Not supported RangeType")
        return subPath
    def _exec(self, urls):
        loop = get_event_loop()
        rr = loop.run_until_complete(self._execAsync(urls))
        return rr
    async def _execAsync(self, urls):
            with self._client as c:
                res = await asyncio.gather(*[self._requestExecutor.exec(c.exec, 'GET', i, None) for i in urls])
                return list(itertools.chain(*map(lambda r: r.json(),res)))
    def __toUrlParam(self, start, end):
        return f"{start}/{end}"
    def _validateQuery(self):
        if(self._queryParameters.extractionRangeType is None):
            raise Exception("Data extraction range must be provided. Provide a date range , period or period range or an interval eg .InAbsoluteDateRange()")
        if(self._queryParameters.ids is None and self._queryParameters.filterId is None):
            raise Exception("Marketadata ids OR filterId must be provided for extraction. Use .ForMarketData() OR .ForFilterId() and provide an integer or integer array as an argument")
    def __getRelativeInterval(self,interval):
        switcher = {
            RelativeInterval.ROLLING_WEEK : "RollingWeek",
            RelativeInterval.ROLLING_YEAR : "RollingYear",
            RelativeInterval.WEEK_TO_DATE : "WeekToDate",
            RelativeInterval.MONTH_TO_DATE : "MonthToDate",
            RelativeInterval.QUARTER_TO_DATE : "QuarterToDate",
            RelativeInterval.ROLLING_MONTH : "RollingMonth",
            RelativeInterval.ROLLING_QUARTER : "RollingQuarter",
            RelativeInterval.YEAR_TO_DATE : "YearToDate"

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