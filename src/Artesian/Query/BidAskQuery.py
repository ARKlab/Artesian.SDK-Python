from __future__ import annotations
from urllib import parse
from Artesian.Query._QueryParameters.QueryParameters import (
    _FillCustomBidAskStrategy,
    _FillLatestStrategy,
    _NoFillStrategy,
    _NullFillStrategy,
)
from ._Query import _Query
from ._QueryParameters.BidAskQueryParameters import BidAskQueryParameters
from .DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from .RelativeInterval import RelativeInterval
from typing import List


class BidAskQuery(_Query):
    __routePrefix = "ba"

    def __init__(
        self: BidAskQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _BidAskQuery"""

        queryParameters = BidAskQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy

    def forMarketData(self: BidAskQuery, ids: List[int]) -> BidAskQuery:
        """
        Set the list of marketdata to be queried.

        Args:
            ids: list of marketdata id's to be queried. Ex.: 100000xxx.

        Results:
            BidAskQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self: BidAskQuery, filterId: int) -> BidAskQuery:
        """
        Sets the list of filtered marketdata id to be queried

        Args:
            filterId: marketdata filtered by id.

        Results:
            BidAskQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self: BidAskQuery, tz: str) -> BidAskQuery:
        """
        Gets the BidAsk Query in a specific TimeZone in IANA format.

        Args:
            tz: "UTC","CET","Europe/Istanbul"

        Results:
            BidAskQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self: BidAskQuery, start: str, end: str) -> BidAskQuery:
        """
        Gets the BidAsk Query in an absolute date range window.
        The Absolute Date Range is in ISO8601 format.

        Args:
            start: string for the date start of the range of extracted timeserie,
                   in ISO format. (ex.: "2022-01-01")

            end: string for the EXCLUSIVE date end of the range of extracted timeserie,
                 in ISO format. (ex.: "2022-01-01")

        Results:
            BidAskQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(self: BidAskQuery, pStart: str, pEnd: str) -> BidAskQuery:
        """
        Gets the BidAsk Query in a relative period range time window.

        Args:
            pStart: string for the relative period start of the range of extracted
                    timeseries. (ex.: "P-3D")

            pEnd: string for the relative period end of the range of the extracted
                  timeseries. (ex.: "P10D")

        Results:
            BidAskQuery.
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self: BidAskQuery, extractionPeriod: str) -> BidAskQuery:
        """
        Gets the BidAsk Query in a relative period of a time window.

        Args:
            extractionPeriod: string for the relative period of extracted timeseries.
                              (ex.: "P5D")

        Results:
            BidAskQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def inRelativeInterval(
        self: BidAskQuery, relativeInterval: RelativeInterval
    ) -> BidAskQuery:
        """
        Gets the Relative Interval considers a specific interval of time window.

        Args:
            relativeInterval: Enum for the relative interval of extracted timeseries.
                              (ex.: "RelativeInterval.ROLLING_WEEK")

        Results:
            BidAskQuery.
        """
        super()._inRelativeInterval(relativeInterval)
        return self

    def forProducts(self: BidAskQuery, products: List[str]) -> BidAskQuery:
        """
        Gets the Products tor the BidAsk Query in a time window.

        Args:
            products: list of string ex.: ["D+1","Feb-18"]

        Results:
            BidAskQuery.
        """
        self._queryParameters.products = products
        return self

    def withFillNull(self: BidAskQuery) -> BidAskQuery:
        """
        Optional filler strategy for the extraction.

          ex.:  withFillNull()

        Results:
          BidAskQuery.
        """
        self._queryParameters.fill = _NullFillStrategy()
        return self

    def withFillNone(self: BidAskQuery) -> BidAskQuery:
        """
        Optional filler strategy for the extraction.

           ex.:  withFillNone()

        Results:
            BidAskQuery.
        """
        self._queryParameters.fill = _NoFillStrategy()
        return self

    def withFillLatestValue(
        self: BidAskQuery, period: str, continueToEnd: bool = False
    ) -> BidAskQuery:
        """
        Optional filler strategy for the extraction.

        Args:
            period: string of the last period value to fill in case there are
                    missing values. Ex.:  .withFillLatestValue("P5D")
            continueToEnd: true means the fill extends to the end of the period even
                           if there's no value at the end of the period
                           false means the fill is only extended to the next valid value

        Results:
            BidAskQuery.
        """
        self._queryParameters.fill = _FillLatestStrategy(period, continueToEnd)
        return self

    def withFillCustomValue(self: BidAskQuery, **val: float) -> BidAskQuery:
        """
        Optional filler strategy for the extraction.

        Args:
            val: float value to fill in case there are missing values.

            Ex.  .withFillCustomValue(
                 bestBidPrice = 1,
                 bestAskPrice = 2,
                 bestBidQuantity = 3,
                 bestAskQuantity = 4,
                 lastPrice = 5,
                 lastQuantity = 6)
        """
        self._queryParameters.fill = _FillCustomBidAskStrategy(**val)
        return self

    def execute(self: BidAskQuery) -> list:
        """
        Execute the Query.

        Returns:
            list of BidAskQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self: BidAskQuery) -> list:
        """
        Execute Async Query.

        Returns:
            list of BidAskQuery."""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self: BidAskQuery) -> List[str]:
        self.__validateQuery()
        qps = self.__partition.PartitionBidAsk([self._queryParameters])
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

    def __validateQuery(self: BidAskQuery) -> None:
        super()._validateQuery()
        if self._queryParameters.products is None:
            raise Exception(
                "Products must be provided for extraction. Use .ForProducts() argument "
                + "takes a string or string array of products"
            )
