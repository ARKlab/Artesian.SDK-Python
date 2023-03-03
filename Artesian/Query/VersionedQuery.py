from __future__ import annotations
from typing import List, Optional
from urllib import parse
from Artesian.Exceptions import ArtesianSdkException
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from .DefaultPartitionStrategy import DefaultPartitionStrategy
from ._Query import _Query
from Artesian.Query._QueryParameters.QueryParameters import _FillCustomMasStrategy, _FillCustomTimeserieStrategy, _FillLatestStrategy, _NoFillStrategy, _NullFillStrategy
from ._QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from ._QueryParameters.ExtractionRangeConfig import ExtractionRangeConfig
from ._QueryParameters.VersionSelectionType import VersionSelectionType
from .RelativeInterval import RelativeInterval
from Artesian.MarketData import Granularity


class VersionedQuery(_Query):
    __routePrefix = "vts"

    def __init__(self, client: _Client,
                 requestExecutor: _RequestExecutor,
                 partitionStrategy: DefaultPartitionStrategy) -> None:
        """ Inits _VersionedQuery """

        queryParameters = VersionedQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy
        

    def forMarketData(self, ids: List[int]) -> VersionedQuery:
        """ Set the list of marketdata to be queried.

            Args:
                ids: list of marketdata id's to be queried. Ex.: 100000xxx

            Returns: 
                VersionedQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self, filterId: int) -> VersionedQuery:
        """ Sets the list of filtered marketdata id to be queried

            Args:
                filterId: marketdata filtered by id

            Returns: 
                VersionedQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self, tz: str) -> VersionedQuery:
        """ Gets the Versioned Query in a specific TimeZone in IANA format.

            Args:
                timezone: "UTC","CET","Europe/Istanbul"

            Returns: 
                VersionedQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self, start: str, end: str) -> VersionedQuery:
        """ Gets the Versioned Query in an absolute date range window. 
            The Absolute Date Range is in ISO8601 format.

            Args:
                start: string for the date start of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")
                end: string for the EXCLUSIVE date end of the range of extracted timeserie, in ISO format. (ex.: "2022-01-01")

            Returns: 
                VersionedQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(self, pStart: str, pEnd: str) -> VersionedQuery:
        """ Gets the Versioned Query in a relative period range time window.

            Args:
                pStart: string for the relative period start of the range of extracted timeseries. (ex.: "P--3D")
                pEnd: string for the relative period end of the range of the extracted timeseries. (ex.: "P10D") 

            Returns: 
                VersionedQuery.
        """
        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self, extractionPeriod: str) -> VersionedQuery:
        """ Gets the Versioned Query in a relative period of a time window.

            Args:
                extractionPeriod: string the relative period of extracted timeseries. (ex.: "P5D")

            Returns: 
                VersionedQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def inRelativeInterval(self, relativeInterval: RelativeInterval) -> VersionedQuery:
        """ Gets the Relative Interval considers a specific interval of time window.

            Args:
                relativeInterval: ENUM. the relative interval of extracted timeseries. (ex.: "RelativeInterval.ROLLING_WEEK" or "RelativeInterval.ROLLING_MONTH") 

            Returns: 
                VersionedQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self

    def withTimeTransform(self, tr: str) -> VersionedQuery:
        """ Gets the Versioned query in a specific Time Transform.

            Args:
                tr: "Custom","GASDAY66","THERMALYEAR"

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.transformId = tr
        return self

    def inGranularity(self, granularity: Granularity) -> VersionedQuery:
        """ Gets the Versioned Query in a specific Granularity.

            Args:
                granularity: Enum ex.: "TenMinute", "FifteenMinute", "Hour", "Year"

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.granularity = granularity
        return self

    def forMUV(self, versionLimit: Optional[str] = None) -> VersionedQuery:
        """ Gets the timeseries of the most updated version of each timepoint of a versioned timeseries.

            Args:
                versionLimit: int from which the most updated version should be taken Ex.: versionLimit("2021-03-12T14:30:00")

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.versionLimit = versionLimit
        self._queryParameters.versionSelectionType = VersionSelectionType.MUV
        return self

    def forLastOfDays(self, start: str, end: Optional[str] = None) -> VersionedQuery:
        """ Gets the lastest version of a versioned timeseries of each day in a time window..

            Args:
                start: string for the start timeseries for last of days. (ex.: forLastOfDays("2021-03-12",...),forLastOfDays("P0Y0M-2D", ...)
                end: string for the end timeseries for last of days. (ex.: forLastOfDays("2021-03-12","2021-03-16")), forLastOfDays("P0Y0M-2D","P0Y0M2D"))

            Returns: 
                VersionedQuery.
        """

        self._queryParameters.versionSelectionType = VersionSelectionType.LastOfDays
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

    def forLastOfMonths(self, start: str, end: Optional[str] = None) -> VersionedQuery:
        """ Gets the lastest version of a versioned timeseries of each month in a time window.

            Args:
                start: string for the start timeseries for last of month. ( ex. forLastOfMonths("2021-03-12",...), forLastOfMonths("P0Y-1M0D",...) 
                end: string for the end timeseries for last of month. (ex. forLastOfMonths("2021-03-12","2021-03-16"), forLastOfMonths("P0Y-1M0D","P0Y1M0D")) 

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.LastOfMonths
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

    def forLastNVersions(self, lastN: int) -> VersionedQuery:
        """ Gets the lastest N timeseries versions that have at least a not-null value .

            Args:
                lastN: an int > 0. Ex.: forLastNVersions(2)

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.LastN
        self._queryParameters.versionSelectionConfig.lastN = lastN
        return self

    def forVersion(self, version: str) -> VersionedQuery:
        """ Gets the specified version of a versioned timeseries.

            Args:
                version: string of a specific version. Ex.: forVersion("2021-03-12T14:30:00")

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.Version
        self._queryParameters.versionSelectionConfig.version = version
        return self

    def forMostRecent(self, start: str, end: Optional[str] = None) -> VersionedQuery:
        """ Gets the most recent version of a versioned timeseries in a time window.

            Args:
                start: string for the start of the most recent version. Ex.: (forMostRecent("2021-03-12",...))

                end: string for the end of the most recent version. Ex.: (forMostRecent("2021-03-12","2021-03-16")) 

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.MostRecent
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

    def withFillNull(self) -> VersionedQuery:
        """ Optional filler strategy for the extraction.

                ex. withFillNull() 

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.fill = _NullFillStrategy()
        return self

    def withFillNone(self) -> VersionedQuery:
        """ Optional filler strategy for the extraction.

                ex. withFillNone() 

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.fill = _NoFillStrategy()
        return self

    def withFillLatestValue(self, period: str, continueToEnd: bool = False) -> VersionedQuery:
        """ Optional filler strategy for the extraction.

            Args:
                period: string of the last period value to fill in case there are missing values. Ex.:   withFillLatestValue("P5D") 
                continueToEnd: true means the fill extends to the end of the period even if there's no value at the end of the period
                               false means the fill is only extended to the next valid value

            Returns: 
                VersionedQuery.
        """
        self._queryParameters.fill = _FillLatestStrategy(period, continueToEnd)
        return self

    def withFillCustomValue(self, val: float) -> VersionedQuery:
        """ Optional filler strategy for the extraction.

            Args:
               val: float value to fill in case there are missing values. Ex.: .withFillCustomValue(10)

            Returns: 
                VersionedQuery.
         """
        self._queryParameters.fill = _FillCustomTimeserieStrategy(val)
        return self

    def execute(self) -> list:
        """ 
            Execute the Query.

            Returns:
                list of VersionedQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self) -> list:
        """ 
            Execute Async Query.

            Returns:
                list of VersionedQuery"""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self):
        self.__validateQuery()
        qps = self.__partition.PartitionVersioned([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{self.__buildVersionRoute()}/{self.__getGranularityPath(qp.granularity)}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids = sep.join(map(str, qp.ids))
                enc = parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + '&filterId=' + 'qp.filterId'
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            if not (qp.transformId is None):
                url = url + "&tr=" + qp.transformId
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            if not (qp.versionLimit is None):
                url = url + "&versionLimit=" + qp.versionLimit
            urls.append(url)
        return urls

    def __validateQuery(self):
        super()._validateQuery()
        if (self._queryParameters.granularity is None):
            raise Exception(
                "Extraction granularity must be provided. Use .InGranularity() argument takes a granularity type")
        if (self._queryParameters.versionSelectionType is None):
            raise Exception(
                "Version selection must be provided. Provide a version to query. eg .ForLastOfDays() arguments take a date range , period or period range")

    def __buildVersionRoute(self):
        switcher = {
            VersionSelectionType.LastN: f"Last{self._queryParameters.versionSelectionConfig.lastN}",
            VersionSelectionType.MUV: f"Muv",
            VersionSelectionType.LastOfDays: f"LastOfDays/" + self.__buildVersionRange(),
            VersionSelectionType.LastOfMonths: f"LastOfMonths/" + self.__buildVersionRange(),
            VersionSelectionType.MostRecent: f"MostRecent/" + self.__buildVersionRange(),
            VersionSelectionType.Version: f"Version/{self._queryParameters.versionSelectionConfig.version}"
        }
        assert self._queryParameters.versionSelectionType is not None
        vr = switcher.get(self._queryParameters.versionSelectionType, "VType")
        if vr == "VType":
            raise Exception("Not supported VersionType")
        return vr

    def __buildVersionRange(self):
        vr = ""
        if (self._queryParameters.versionSelectionConfig.versionsRange.dateStart is not None) and (self._queryParameters.versionSelectionConfig.versionsRange.dateEnd is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.period is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.period}"
        elif (self._queryParameters.versionSelectionConfig.versionsRange.periodFrom is not None) and (self._queryParameters.versionSelectionConfig.versionsRange.periodTo is not None):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.dateStart}/{self._queryParameters.versionSelectionConfig.versionsRange.dateEnd}"
        return vr

    def __getGranularityPath(self, granularity:Optional[Granularity]) -> str:
        switcher = {
            Granularity.Day: "Day",
            Granularity.FifteenMinute: "FifteenMinute",
            Granularity.Hour: "Hour",
            Granularity.Minute: "Minute",
            Granularity.Month: "Month",
            Granularity.Quarter: "Quarter",
            Granularity.TenMinute: "TenMinute",
            Granularity.ThirtyMinute: "ThirtyMinute",
            Granularity.Week: "Week",
            Granularity.Year: "Year",
        }
        if granularity is None:
            raise ArtesianSdkException("Missing Granularity. Use .forGranularity() to set one.")
        
        vr = switcher.get(granularity, "VGran")
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
