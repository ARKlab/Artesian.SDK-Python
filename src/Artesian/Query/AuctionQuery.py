from __future__ import annotations
from urllib import parse
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian.Query.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian.Query._Query import _Query
from Artesian.Query._QueryParameters.AuctionQueryParameters import (
    AuctionQueryParameters,
)
from typing import List


class AuctionQuery(_Query):
    __routePrefix = "auction"

    def __init__(
        self: AuctionQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _AuctionQuery"""

        queryParameters = AuctionQueryParameters()
        _Query.__init__(self, client, requestExecutor, queryParameters)
        self._queryParameters = queryParameters
        self.__partition = partitionStrategy

    def forMarketData(self: AuctionQuery, ids: List[int]) -> AuctionQuery:
        """
        Set the list of marketdata to be queried.

        Args:
            ids: list of marketdata id's to be queried. Ex.: 100000xxx

        Returns:
            AuctionQuery.
        """
        super()._forMarketData(ids)
        return self

    def forFilterId(self: AuctionQuery, filterId: int) -> AuctionQuery:
        """
        Sets the list of filtered marketdata id to be queried

        Args:
            filterId: marketdata filtered by id.

        Returns:
            AuctionQuery.
        """
        super()._forFilterId(filterId)
        return self

    def inTimeZone(self: AuctionQuery, tz: str) -> AuctionQuery:
        """
        Gets the Auction Query in a specific TimeZone in IANA format.

        Args:
            tz: "UTC","CET","Europe/Istanbul"

        Returns:
            AuctionQuery.
        """
        super()._inTimezone(tz)
        return self

    def inAbsoluteDateRange(self: AuctionQuery, start: str, end: str) -> AuctionQuery:
        """
        Gets the Auction Query in an absolute date range window.
        The Absolute Date Range is in ISO8601 format.

        Args:
            start: string for the date start of the range of extracted timeserie,
                   in ISO format. (ex.: "2022-01-01")

            end:  string for the EXCLUSIVE date end of the range of extracted timeserie,
                  in ISO format. (ex.: "2022-01-01")

        Returns:
            AuctionQuery.
        """
        super()._inAbsoluteDateRange(start, end)
        return self

    def inRelativePeriodRange(
        self: AuctionQuery, pStart: str, pEnd: str
    ) -> AuctionQuery:
        """
        Gets the Auction Query in a relative period range time window.

        Args:
            pStart: string for the relative period start of the range of extracted
                    timeseries. (ex.: "P-3D")

            pEnd: string for the relative period end of the range of the extracted
                  timeseries. (ex.: "P10D")

        Returns:
            AuctionQuery.
        """

        super()._inRelativePeriodRange(pStart, pEnd)
        return self

    def inRelativePeriod(self: AuctionQuery, extractionPeriod: str) -> AuctionQuery:
        """
        Gets the Auction Query in a relative period of a time window.

        Args:
            extractionPeriod: string for the relative period of extracted
                              timeseries. (ex.: "P5D")

        Returns:
            AuctionQuery.
        """
        super()._inRelativePeriod(extractionPeriod)
        return self

    def execute(self: AuctionQuery) -> list:
        """
        Execute the Query.

        Returns:
            list of AuctionQuery."""
        urls = self.__buildRequest()
        return super()._exec(urls)

    async def executeAsync(self: AuctionQuery) -> list:
        """
        Execute Async Query.

        Returns:
            list of AuctionQuery."""
        urls = self.__buildRequest()
        return await super()._execAsync(urls)

    def __buildRequest(self: AuctionQuery) -> List[str]:
        self.__validateQuery()
        qps = self.__partition.PartitionAuction([self._queryParameters])
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
            if not (qp.timezone is None):
                url = url + "&tz=" + qp.timezone
            urls.append(url)
        return urls

    def __validateQuery(self: AuctionQuery) -> None:
        super()._validateQuery()
        if self._queryParameters.ids is None and self._queryParameters.filterId is None:
            raise Exception(
                "Extraction ids or filterid must be provided. Use .forMarketData() "
                + "or .forFilterId()"
            )
