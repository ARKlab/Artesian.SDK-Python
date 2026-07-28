from __future__ import annotations
from Artesian.Exceptions import ArtesianSdkException
from Artesian.Query._QueryParameters.QueryParameters import (
    _FillCustomTimeserieStrategy,
    _FillLatestStrategy,
    _NoFillStrategy,
    _NullFillStrategy,
)
from .._ClientsExecutor.RequestExecutor import _RequestExecutor
from .._ClientsExecutor.Client import _Client
from .DefaultPartitionStrategy import DefaultPartitionStrategy
from ._Query import _Query
from .RelativeInterval import RelativeInterval
from ._QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian.MarketData import Granularity
from Artesian.MarketData import AggregationRule
from urllib import parse
from typing import List, Optional


class ActualQuery(_Query):
    __routePrefix = "ts"

    def __init__(
        self: ActualQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _ActualQuery"""

        queryParameters = ActualQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy

    def forMarketData(self: ActualQuery, ids: List[int]) -> ActualQuery:
        """
        Set the list of marketdata to be queried.

        Args:
            ids: list of marketdata id's to be queried. Ex.: 100000xxx

        Returns:
            ActualQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self: ActualQuery, filterId: int) -> ActualQuery:
        """
        Sets the list of filtered marketdata id to be queried

        Args:
            filterId: marketdata filtered by id to be queried.

        Returns:
            ActualQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self: ActualQuery, tz: str) -> ActualQuery:
        """
        Gets the Actual Query in a specific TimeZone in IANA format.

        Args:
            tz: "UTC","CET","Europe/Istanbul"

        Returns:
            ActualQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self: ActualQuery, start: str, end: str) -> ActualQuery:
        """
        Gets the Actual Query in an absolute date range window.
        The Absolute Date Range is in ISO8601 format.

        Args:
            start: string for the date start of the range of extracted timeserie,
                   in ISO format. (ex.: "2022-01-01")

            end: string for the EXCLUSIVE date end of the range of extracted timeserie,
                 in ISO format. (ex.: "2022-01-01")

        Returns:
            ActualQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(self: ActualQuery, pStart: str, pEnd: str) -> ActualQuery:
        """
        Gets the Actual Query in a relative period range time window.

        Args:
            pStart: string for the relative period start of the range of extracted
                    timeseries. (ex.: "P-3D")

            pEnd: string for the relative period end of the range of the extracted
                  timeseries. (ex.: "P10D")

        Returns:
            ActualQuery.
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self: ActualQuery, extractionPeriod: str) -> ActualQuery:
        """
         Gets the Actual Query in a relative period of a time window.

         Args:
             extractionPeriod: string for the relative period of extracted timeseries.
                               (ex.: "P5D")

        Returns:
             ActualQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def inRelativeInterval(
        self: ActualQuery, relativeInterval: RelativeInterval
    ) -> ActualQuery:
        """
        Gets the Relative Interval considers a specific interval of time window.

        Args:
            relativeInterval: Enum for the relative interval of extracted timeseries.
                              (ex.: "RelativeInterval.ROLLING_WEEK")

        Returns:
            ActualQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self

    def withTimeTransform(self: ActualQuery, tr: str) -> ActualQuery:
        """
        Gets the Actual Query in a specific time transform to be queried.

        Args:
            tr: "Custom", "GASDAY66", "THERMALYEAR"

        Returns:
            ActualQuery.
        """
        self._queryParameters.transformId = tr
        return self

    def inGranularity(self: ActualQuery, granularity: Granularity) -> ActualQuery:
        """
        Gets the Actual Query in a specific granularity to be queried.

        Args:
            granularity: Enum ex.: "TenMinute", "FifteenMinute", "Hour", "Year"

        Returns:
            ActualQuery.
        """
        self._queryParameters.granularity = granularity
        return self

    def withFillNull(self: ActualQuery) -> ActualQuery:
        """
        Optional filler strategy for the extraction.

            ex.: withFillNull()

        Returns:
            ActualQuery.
        """
        self._queryParameters.fill = _NullFillStrategy()
        return self

    def withFillNone(self: ActualQuery) -> ActualQuery:
        """
        Optional filler strategy for the extraction.

            ex.: withFillNone()

        Returns:
            ActualQuery.
        """
        self._queryParameters.fill = _NoFillStrategy()
        return self

    def withFillLatestValue(
        self: ActualQuery, period: str, continueToEnd: bool = False
    ) -> ActualQuery:
        """
        Optional filler strategy for the extraction.

        Args:
            period: string of the last period value to fill in case there are missing
                    values. Ex.: withFillLatestValue("P5D")
            continueToEnd: true means the fill value extends to the end of the period
                           even if there's no value at the end of the period
                           false means the fill is only extended to the next valid value

        Returns:
            ActualQuery.
        """
        self._queryParameters.fill = _FillLatestStrategy(period, continueToEnd)
        return self

    def withFillCustomValue(self: ActualQuery, value: float) -> ActualQuery:
        """
        Optional filler strategy for the extraction.

        Args:
            value: float value to fill in case there are missing values.
                   Ex.: .withFillCustomValue(10)

        Returns:
            ActualQuery.
        """
        self._queryParameters.fill = _FillCustomTimeserieStrategy(value)
        return self

    def inUnitOfMeasure(self: ActualQuery, unitOfMeasure: str) -> ActualQuery:
        """
        Gets the Actual Query in a specific unit of measure to be queried.

        Args:
            unitOfMeasure: str ex.: "MW", "MWh", "kW/day", "km"

        Returns:
            ActualQuery.
        """
        self._queryParameters.unitOfMeasure = unitOfMeasure
        return self

    def withAggregationRule(self: ActualQuery,
                            aggregationRule: AggregationRule) -> ActualQuery:
        """
        Optional AggregationRule for the extraction.

        Args:
            aggregationRule: enum AggregationRule ex.: "SumAndDivide",
                                                       "AverageAndReplicate"

        Returns:
            ActualQuery.
        """
        self._queryParameters.aggregationRule = aggregationRule
        return self

    def execute(self: ActualQuery) -> list:
        """
        Execute the Query.

        Returns:
            list of ActualQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self: ActualQuery) -> list:
        """
        Execute Async Query.

        Returns:
            list of ActualQuery."""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self: ActualQuery) -> List[str]:
        self.__validateQuery()
        qps = self.__partition.PartitionActual([self._queryParameters])
        urls = []
        for qp in qps:
            url = "/{0}/{1}/{2}?_=1".format(
                self.__routePrefix,
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
                url = url + "&tr=" + str(qp.transformId)
            if not (qp.unitOfMeasure is None):
                url = url + "&unitOfMeasure=" + qp.unitOfMeasure
            if not (qp.aggregationRule is None):
                url = url + "&aggregationRule=" + str(qp.aggregationRule)
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls

    def __validateQuery(self: ActualQuery) -> None:
        super()._validateQuery()
        if self._queryParameters.granularity is None:
            raise Exception(
                "Extraction granularity must be provided. Use .InGranularity() "
                + "argument takes a granularity type"
            )

    def __getGranularityPath(
        self: ActualQuery, granularity: Optional[Granularity]
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
