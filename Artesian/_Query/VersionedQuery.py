from Artesian._Query.Query import _Query
from Artesian._Query.QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from Artesian._Query.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.VersionSelectionType import VersionSelectionType
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._Query.Config.Granularity import Granularity
import urllib
class _VersionedQuery(_Query):
    __routePrefix = "vts"
    def __init__(self, client, requestExecutor, partitionStrategy):
        """ Inits _VersionedQuery 

            Args:
            
                client credential

                requestExecutor

                partitionStrategy. """

        queryParameters = VersionedQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None, None, None) 
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
        """ Gets the Versioned Query in a specific TimeZone.

            E.g.: (UTC") / ("CET") / ("EET") / ("WET") / ("Europe/Istanbul") / ("Europe/Moscow")"""
        super()._inTimezone(tz)
        return self
    def inAbsoluteDateRange(self, start, end):
        """ Gets the Versioned Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.
        
            E.g.: ("2021-12-01", "2021-12-31")
        """
        super()._inAbsoluteDateRange(start, end)
        return self
    def inRelativePeriodRange(self, pStart, pEnd=None):
        """ Gets the Versioned Query in a relative period range time window.
        
        E.g.: ("P-3D", "P10D") -> from 3 days prior, to be considered until 10 days after."""


        super()._inRelativePeriodRange(pStart, pEnd)
        return self
    def inRelativePeriod(self, extractionPeriod):
        """ Gets the Versioned Query in a relative period of a time window.
        
        E.g.: ("P5D")"""
        super()._inRelativePeriod(extractionPeriod)
        return self
    def inRelativeInterval(self, relativeInterval):
        """ The Relative Interval considers a specific interval of time.
        
        E.g.: (RelativeInterval.ROLLING_WEEK) or (RelativeInterval.ROLLING_MONTH)"""
        super()._inRelativeInterval(relativeInterval)
        return self
    def withTimeTransform(self, tr):
        """ With Time Transform:
        
        E.g.: ("Custom") / ("GASDAY66") / ("THERMALYEAR") ."""
        self._queryParameters.transformId = tr
        return self
    def inGranularity(self, granularity):
        """ The Granularity needs to be specified:
        
        E.g.: ("TenMinute") / ("FifteenMinute") / ("Hour") / ("Day") / ("Week") / ("Month") / ("Season") / ("Year") """
        self._queryParameters.granularity = granularity
        return self
    def forMUV(self):
        """ Gets the timeseries of the most updated version of each timepoint of a versioned timeseries.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.MUV
        return self
    def forLastOfDays(self, start, end=None):
        """ Gets the lastest version of a versioned timeseries of each day in a time window..

        E.g.: forLastOfDays("2021-03-12","2021-03-16") / forLastOfDays("P0Y0M-2D","P0Y0M2D") / forLastOfDays("P0Y0M-2D")"""

        self._queryParameters.versionSelectionType = VersionSelectionType.LAST_OF_DAYS      
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
        return self
    def forLastOfMonths(self, start, end=None):
        """ Gets the lastest version of a versioned timeseries of each month in a time window.

        E.g.: forLastOfMonths("2021-03-12","2021-03-16") / forLastOfMonths("P0Y-1M0D","P0Y1M0D") / forLastOfMonths("P0Y-1M0D") """
        self._queryParameters.versionSelectionType = VersionSelectionType.LAST_OF_MONTHS
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
        return self
    def forLastNVersions(self, lastN):
        """ Gets the lastest N timeseries versions that have at least a not-null value .
        
        E.g.: forLastNVersions(2)"""
        self._queryParameters.versionSelectionType = VersionSelectionType.LASTN
        self._queryParameters.versionSelectionConfig.lastN = lastN
        return self
    def forVersion(self, version):
        """ Gets the specified version of a versioned timeseries.
        
        E.g.: forVersion("2021-03-12T14:30:00")"""
        self._queryParameters.versionSelectionType = VersionSelectionType.VERSION
        self._queryParameters.versionSelectionConfig.version = version
        return self
    def forMostRecent(self, start, end=None):
        """ Gets the most recent version of a versioned timeseries in a time window.
        
        E.g.: .forMostRecent("2021-03-12","2021-03-16") / forMostRecent("2021-03-12T12:30:05","2021-03-16T18:42:30") / forMostRecent("P0Y0M-2D","P0Y0M2D") / forMostRecent("P0Y0M-2D") / forMostRecent("2021-03-12","2021-03-16") / forMostRecent("P0Y-1M0D","P0Y1M0D") / forMostRecent("P0Y-1M0D") """
        self._queryParameters.versionSelectionType = VersionSelectionType.MOST_RECENT
        if(start.startswith("P")):
            if(end is None):
                self._queryParameters.versionSelectionConfig.versionsRange.period = start
            else:
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom = start
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo = end
        else:
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart = start
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd = end
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
    def withFillCustomValue(self, val):
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
        qps = self.__partition.Partitionversioned([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{self.__buildVersionRoute()}/{self.__getGranularityPath(qp.granularity)}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids= sep.join(map(str,qp.ids))
                enc = urllib.parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + qp.filterId
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            if not (qp.transformId is None):
                url = url + "&tr=" + qp.transformId
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls
    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.granularity is None):
            raise Exception("Extraction granularity must be provided. Use .InGranularity() argument takes a granularity type")
        if (self._queryParameters.versionSelectionType is None):
            raise Exception("Version selection must be provided. Provide a version to query. eg .ForLastOfDays() arguments take a date range , period or period range")
    def __buildVersionRoute(self):
        switcher = {
            VersionSelectionType.LASTN: f"Last{self._queryParameters.versionSelectionConfig.lastN}",
            VersionSelectionType.MUV: f"MUV",
            VersionSelectionType.LAST_OF_DAYS: f"LastOfDays/" + self.__buildVersionRange(),
            VersionSelectionType.LAST_OF_MONTHS: f"LastOfMonths/" + self.__buildVersionRange(),
            VersionSelectionType.MOST_RECENT: f"MostRecent/" + self.__buildVersionRange(),
            VersionSelectionType.VERSION: f"Version/{self._queryParameters.versionSelectionConfig.version}"
        }
        vr = switcher.get(self._queryParameters.versionSelectionType, "VType")
        if vr == "VType" :
            raise Exception("Not supported VersionType")
        return vr
    def __buildVersionRange(self):
        vr=""
        if  (self._queryParameters.versionSelectionConfig.versionsRange.dateStart is not None) and (self._queryParameters.versionSelectionConfig.versionsRange.dateEnd is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.period is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.period}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.periodFrom is not None) and  (self._queryParameters.versionSelectionConfig.versionsRange.periodTo is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        return vr
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
        return f"fillerK=CustomValue&fillerDV={self.val}"