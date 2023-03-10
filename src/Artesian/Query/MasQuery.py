from __future__ import annotations
from urllib import parse
from Artesian.Query._QueryParameters.QueryParameters import (
    _FillCustomMasStrategy,
    _FillLatestStrategy,
    _NoFillStrategy,
    _NullFillStrategy,
)
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from .DefaultPartitionStrategy import DefaultPartitionStrategy
from ._Query import _Query
from ._QueryParameters.MasQueryParameters import MasQueryParameters
from typing import List

from .RelativeInterval import RelativeInterval


class MasQuery(_Query):
    __routePrefix = "mas"

    def __init__(
        self: MasQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _MasQuery"""

        queryParameters = MasQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy

    def forMarketData(self: MasQuery, ids: List[int]) -> MasQuery:
        """
        Set the list of marketdata to be queried.

        Args:
            ids: list of marketdata id's to be queried. Ex.: 100000xxx

        Returns:
            MasQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self: MasQuery, filterId: int) -> MasQuery:
        """
        Sets the list of filtered marketdata id to be queried

        Args:
            filterId: marketdata filtered by id

        Returns:
            MasQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self: MasQuery, tz: str) -> MasQuery:
        """
        Gets the Mas Query in a specific TimeZone in IANA format.

        Args:
            tz: "UTC","CET","Europe/Istanbul"

        Returns:
            MasQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self: MasQuery, start: str, end: str) -> MasQuery:
        """
        Gets the Mas Query in an absolute date range window.
        The Absolute Date Range is in ISO8601 format.

        Args:
            start: string for the date start of the range of extracted timeserie,
                   in ISO format. (ex.: "2022-01-01")

            end: string for the EXCLUSIVE date end of the range of extracted timeserie,
                 in ISO format. (ex.: "2022-01-01")

        Returns:
            MasQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(self: MasQuery, pStart: str, pEnd: str) -> MasQuery:
        """
        Gets the Mas Query in a relative period range time window.

        Args:
            pStart: string for the relative period start of the range of extracted
                    timeseries. (ex.: "P-3D")

            pEnd: string for the relative period end of the range of the extracted
                  timeseries. (ex.: "P10D")

        Returns:
            MasQuery.
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self: MasQuery, extractionPeriod: str) -> MasQuery:
        """
        Gets the Mas Query in a relative period of a time window.

        Args:
            extractionPeriod: string for the relative period of extracted timeseries.
                              (ex.: "P5D")

        Returns:
            MasQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def inRelativeInterval(
        self: MasQuery, relativeInterval: RelativeInterval
    ) -> MasQuery:
        """
        Gets the Relative Interval considers a specific interval of time window.

        Args:
            relativeInterval: Enum for the relative interval of extracted timeseries.
                              (ex.: "RelativeInterval.ROLLING_WEEK" or
                              "RelativeInterval.ROLLING_MONTH")

        Returns:
            MasQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self

    def forProducts(self: MasQuery, products: List[str]) -> MasQuery:
        """
        Gets the Products tor the BidAsk Query in a time window.

        Args:
            products: list of string ex.: ["D+1","Feb-18"]

        Returns:
            MasQuery.
        """
        self._queryParameters.products = products
        return self

    def withFillNull(self: MasQuery) -> MasQuery:
        """
        Optional filler strategy for the extraction.

            ex.:  withFillNull()

        Returns:
            MasQuery.
        """
        self._queryParameters.fill = _NullFillStrategy()
        return self

    def withFillNone(self: MasQuery) -> MasQuery:
        """
        Optional filler strategy for the extraction.

            ex.:  withFillNone()

        Returns:
            MasQuery.
        """
        self._queryParameters.fill = _NoFillStrategy()
        return self

    def withFillLatestValue(
        self: MasQuery, period: str, continueToEnd: bool = False
    ) -> MasQuery:
        """
        Optional filler strategy for the extraction.

        Args:
            period: string of the last period value to fill in case there are missing
                    values. Ex.: withFillLatestValue("P5D")

            continueToEnd: true means the fill extends to the end of the period even
                           if there's no value at the end of the period
                           false means the fill is only extended to the next valid value
        Returns:
            MasQuery.
        """
        self._queryParameters.fill = _FillLatestStrategy(period, continueToEnd)
        return self

    def withFillCustomValue(self: MasQuery, **val: float) -> MasQuery:
        """
        Optional filler strategy for the extraction.

        Args:
           val: float value to fill in case there are missing values.
                Ex.: .withFillCustomValue(settlement = 1,open = 2,close = 3
                    ,high = 4,low = 5,volumePaid = 6,volueGiven = 7,volume = 8)

        Returns:
            MasQuery.
        """
        self._queryParameters.fill = _FillCustomMasStrategy(**val)
        return self

    def execute(self: MasQuery) -> list:
        """
        Execute the Query.

        Returns:
            list of MasQuery.
        """
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self: MasQuery) -> list:
        """
        Execute Async Query.

        Returns:
            list of MasQuery."""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self: MasQuery) -> List[str]:
        self.__validateQuery()
        qps = self.__partition.PartitionMas([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"/{self.__routePrefix}/{super()._buildExtractionRangeRoute(qp)}?_=1"
            if not (qp.ids is None):
                sep = ","
                ids = sep.join(map(str, qp.ids))
                enc = parse.quote_plus(ids)
                url = url + "&id=" + enc
            if not (qp.filterId is None):
                url = url + "&filterId=" + str(qp.filterId)
            if not (qp.products is None):
                sep = ","
                prod = enc = parse.quote_plus(sep.join(qp.products))
                url = url + "&p=" + prod
            if not (qp.fill is None):
                url = url + "&" + qp.fill.getUrlParams()
            urls.append(url)
        return urls

    def __validateQuery(self: MasQuery) -> None:
        super()._validateQuery()
        if self._queryParameters.products is None:
            raise Exception(
                "Products must be provided for extraction. Use .ForProducts() "
                + "argument takes a string or string array of products"
            )
