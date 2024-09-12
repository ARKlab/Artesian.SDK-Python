from __future__ import annotations
from typing import List, Optional
from urllib import parse
from Artesian.Exceptions import ArtesianSdkException
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from .DefaultPartitionStrategy import DefaultPartitionStrategy
from ._Query import _Query
from Artesian.Query._QueryParameters.QueryParameters import (
    _FillCustomTimeserieStrategy,
    _FillLatestStrategy,
    _NoFillStrategy,
    _NullFillStrategy,
)
from ._QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from ._QueryParameters.VersionSelectionType import VersionSelectionType
from .RelativeInterval import RelativeInterval
from Artesian.MarketData import Granularity


class DerivedQuery(_Query):
    __routePrefix = "vts"

    def __init__(
        self: DerivedQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _DerivedQuery"""

        queryParameters = VersionedQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy

    def forMarketData(self: DerivedQuery, ids: List[int]) -> DerivedQuery:
        """Set the list of marketdata to be queried.

        Args:
            ids: list of marketdata id's to be queried. Ex.: 100000xxx

        Returns:
            DerivedQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self: DerivedQuery, filterId: int) -> DerivedQuery:
        """Sets the list of filtered marketdata id to be queried

        Args:
            filterId: marketdata filtered by id

        Returns:
            DerivedQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self: DerivedQuery, tz: str) -> DerivedQuery:
        """Gets the Derived Query in a specific TimeZone in IANA format.

        Args:
            timezone: "UTC","CET","Europe/Istanbul"

        Returns:
            DerivedQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self: DerivedQuery, start: str, end: str) -> DerivedQuery:
        """Gets the Derived Query in an absolute date range window.
        The Absolute Date Range is in ISO8601 format.

        Args:
            start: string for the date start of the range of extracted timeserie,
                   in ISO format. (ex.: "2022-01-01")
            end: string for the EXCLUSIVE date end of the range of extracted timeserie,
                 in ISO format. (ex.: "2022-01-01")

        Returns:
            DerivedQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(
        self: DerivedQuery, pStart: str, pEnd: str
    ) -> DerivedQuery:
        """Gets the Derived Query in a relative period range time window.

        Args:
            pStart: string for the relative period start of the range of extracted
                    timeseries. (ex.: "P--3D")
            pEnd: string for the relative period end of the range of the extracted
                  timeseries. (ex.: "P10D")

        Returns:
            DerivedQuery.
        """
        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self: DerivedQuery, extractionPeriod: str) -> DerivedQuery:
        """Gets the Derived Query in a relative period of a time window.

        Args:
            extractionPeriod: string the relative period of extracted timeseries.
                              (ex.: "P5D")

        Returns:
            DerivedQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def inRelativeInterval(
        self: DerivedQuery, relativeInterval: RelativeInterval
    ) -> DerivedQuery:
        """Gets the Relative Interval considers a specific interval of time window.

        Args:
            relativeInterval: ENUM. the relative interval of extracted timeseries.
                              (ex.: "RelativeInterval.ROLLING_WEEK")

        Returns:
            DerivedQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self

    def withTimeTransform(self: DerivedQuery, tr: str) -> DerivedQuery:
        """Gets the Derived query in a specific Time Transform.

        Args:
            tr: "Custom","GASDAY66","THERMALYEAR"

        Returns:
            DerivedQuery.
        """
        self._queryParameters.transformId = tr
        return self

    def inGranularity(self: DerivedQuery, granularity: Granularity) -> DerivedQuery:
        """Gets the Derived Query in a specific Granularity.

        Args:
            granularity: Enum ex.: "TenMinute", "FifteenMinute", "Hour", "Year"

        Returns:
            DerivedQuery.
        """
        self._queryParameters.granularity = granularity
        return self

    def forDerived(self: DerivedQuery) -> DerivedQuery:
        """Gets the timeseries of the most updated version of each timepoint of
           a derived marketdata based on the provided configuration.

        Returns:
            DerivedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.MUV
        return self

    def withFillNull(self: DerivedQuery) -> DerivedQuery:
        """Optional filler strategy for the extraction.

            ex. withFillNull()

        Returns:
            DerivedQuery.
        """
        self._queryParameters.fill = _NullFillStrategy()
        return self

    def withFillNone(self: DerivedQuery) -> DerivedQuery:
        """Optional filler strategy for the extraction.

            ex. withFillNone()

        Returns:
            DerivedQuery.
        """
        self._queryParameters.fill = _NoFillStrategy()
        return self

    def withFillLatestValue(
        self: DerivedQuery, period: str, continueToEnd: bool = False
    ) -> DerivedQuery:
        """Optional filler strategy for the extraction.

        Args:
            period: string of the last period value to fill in case there are missing
                    values. Ex.:   withFillLatestValue("P5D")
            continueToEnd: true means the fill extends to the end of the period even
                           if there's no value at the end of the period
                           false means the fill is only extended to the next valid value

        Returns:
            DerivedQuery.
        """
        self._queryParameters.fill = _FillLatestStrategy(period, continueToEnd)
        return self

    def withFillCustomValue(self: DerivedQuery, val: float) -> DerivedQuery:
        """Optional filler strategy for the extraction.

        Args:
           val: float value to fill in case there are missing values.
                Ex.: .withFillCustomValue(10)

        Returns:
            DerivedQuery.
        """
        self._queryParameters.fill = _FillCustomTimeserieStrategy(val)
        return self

    def execute(self: DerivedQuery) -> list:
        """
        Execute the Query.

        Returns:
            list of VersionedQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self: DerivedQuery) -> list:
        """
        Execute Async Query.

        Returns:
            list of DerivdQuery"""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self: DerivedQuery) -> List[str]:
        self.__validateQuery()
        qps = self.__partition.PartitionVersioned([self._queryParameters])
        urls = []
        for qp in qps:
            url = "/{0}/{1}/{2}/{3}?_=1".format(
                self.__routePrefix,
                self.__buildVersionRoute(),
                self.__getGranularityPath(qp.granularity),
                super()._buildExtractionRangeRoute(qp),
            )
            if not (qp.ids is None):
                sep = ","
                ids = sep.join(map(str, qp.ids))
                enc = parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + str(qp.filterId)
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

    def __validateQuery(self: DerivedQuery) -> None:
        super()._validateQuery()
        if self._queryParameters.granularity is None:
            raise Exception(
                "Extraction granularity must be provided. Use .InGranularity() "
                + "argument takes a granularity type"
            )
        if self._queryParameters.versionSelectionType is None:
            raise Exception(
                "Version selection must be provided. Provide a version to query. "
                + "eg .ForLastOfDays() arguments take a date range, period or range"
            )

    def __buildVersionRoute(self: DerivedQuery) -> str:
        lastN = f"Last{self._queryParameters.versionSelectionConfig.lastN}"
        version = f"Version/{self._queryParameters.versionSelectionConfig.version}"
        switcher = {
            VersionSelectionType.LastN: lastN,
            VersionSelectionType.MUV: "Muv",
            VersionSelectionType.LastOfDays: "LastOfDays/" + self.__buildVersionRange(),
            VersionSelectionType.LastOfMonths: "LastOfMonths/"
            + self.__buildVersionRange(),
            VersionSelectionType.MostRecent: "MostRecent/" + self.__buildVersionRange(),
            VersionSelectionType.Version: version,
        }
        assert self._queryParameters.versionSelectionType is not None
        vr = switcher.get(self._queryParameters.versionSelectionType, "VType")
        if vr == "VType":
            raise Exception("Not supported VersionType")
        return vr

    def __buildVersionRange(self: DerivedQuery) -> str:
        vr = ""
        if (
            self._queryParameters.versionSelectionConfig.versionsRange.dateStart
            is not None
        ) and (
            self._queryParameters.versionSelectionConfig.versionsRange.dateEnd
            is not None
        ):
            vr = "{0}/{1}".format(
                self._queryParameters.versionSelectionConfig.versionsRange.dateStart,
                self._queryParameters.versionSelectionConfig.versionsRange.dateEnd,
            )
        elif (
            self._queryParameters.versionSelectionConfig.versionsRange.period
            is not None
        ):
            vr = f"{self._queryParameters.versionSelectionConfig.versionsRange.period}"
        elif (
            self._queryParameters.versionSelectionConfig.versionsRange.periodFrom
            is not None
        ) and (
            self._queryParameters.versionSelectionConfig.versionsRange.periodTo
            is not None
        ):
            vr = "{0}/{1}".format(
                self._queryParameters.versionSelectionConfig.versionsRange.periodFrom,
                self._queryParameters.versionSelectionConfig.versionsRange.periodTo,
            )
        return vr

    def __getGranularityPath(
        self: DerivedQuery, granularity: Optional[Granularity]
    ) -> str:
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
            raise ArtesianSdkException(
                "Missing Granularity. Use .forGranularity() to set one."
            )

        vr = switcher.get(granularity, "VGran")
        return vr


class _NullFillStategy:
    def getUrlParams(self: _NullFillStategy) -> str:
        return "fillerK=Null"


class _NoFillStategy:
    def getUrlParams(self: _NoFillStategy) -> str:
        return "fillerK=NoFill"


class _FillLatestStategy:
    def __init__(self: _FillLatestStategy, period: str) -> None:
        self.period = period

    def getUrlParams(self: _FillLatestStategy) -> str:
        return f"fillerK=LatestValidValue&fillerP={self.period}"
