from __future__ import annotations
import copy
from typing import List, TypeVar

from ._QueryParameters.QueryParameters import _QueryParameters
from ._QueryParameters.ActualQueryParameters import ActualQueryParameters
from ._QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from ._QueryParameters.AuctionQueryParameters import AuctionQueryParameters
from ._QueryParameters.MasQueryParameters import MasQueryParameters
from ._QueryParameters.BidAskQueryParameters import BidAskQueryParameters


T = TypeVar("T", bound=_QueryParameters)


class DefaultPartitionStrategy:
    """Class for the default strategy to partition Query Parameters."""

    maxNumberOfIds = 15
    """ Only 15 allowed."""

    def PartitionActual(
        self: DefaultPartitionStrategy,
        actualQueryParameters: List[ActualQueryParameters],
    ) -> List[ActualQueryParameters]:
        """
        The partition strategy for the Actual Time Series Query.

        Args:
            actualQueryParameters: list of the actual query parameters to partition.
        Returns:
            The input list of Actual Time Series Query parameters partitioned
            with the defined strategy.
        """
        return self._tsPartitionStrategy(actualQueryParameters)

    def PartitionAuction(
        self: DefaultPartitionStrategy,
        auctionQueryParameters: List[AuctionQueryParameters],
    ) -> List[AuctionQueryParameters]:
        """
        The partition strategy for the Auction Time Series Query.

        Args:
            auctionQueryParameters: list of auction query parameters to partition.
        Returns:
            The input list of Auction Time Series Query parameters partitioned
            with the defined strategy.
        """
        return self._tsPartitionStrategy(auctionQueryParameters)

    def PartitionVersioned(
        self: DefaultPartitionStrategy,
        versionedQueryParameters: List[VersionedQueryParameters],
    ) -> List[VersionedQueryParameters]:
        """
        The partition strategy for the Versioned Time Series Query.

        Args:
             versionedQueryParameters: list of versioned query parameters to partition.
        Returns:
             The input list of Versioned Time Series Query parameters partitioned
             with the defined strategy.
        """
        return self._tsPartitionStrategy(versionedQueryParameters)

    def PartitionMas(
        self: DefaultPartitionStrategy, masQueryParameters: List[MasQueryParameters]
    ) -> List[MasQueryParameters]:
        """
        The partition strategy for the Market Assessment Query.

        Args:
            masQueryParameters: list of mas query parameters to partition.
        Returns:
            The input list of Market Assessment Query parameters partitioned
            with the defined strategy.
        """
        return self._tsPartitionStrategy(masQueryParameters)

    def PartitionBidAsk(
        self: DefaultPartitionStrategy,
        bidAskQueryParameters: List[BidAskQueryParameters],
    ) -> List[BidAskQueryParameters]:
        """
        The partition strategy for the Bid Ask Query.

        Args:
            bidAskQueryParameters: list of bid ask query parameters to partition.
        Returns:
            The input list of Bid Ask Query parameters partitioned
            with the defined strategy.
        """
        return self._tsPartitionStrategy(bidAskQueryParameters)

    def _tsPartitionStrategy(
        self: DefaultPartitionStrategy, Parameters: List[T]
    ) -> List[T]:
        res: List[T] = []
        for param in Parameters:
            if param.ids is None:
                res.append(param)
                continue
            leng = len(param.ids)
            batches = [
                param.ids[i : i + DefaultPartitionStrategy.maxNumberOfIds]
                for i in range(0, leng, DefaultPartitionStrategy.maxNumberOfIds)
            ]
            for batch in batches:
                cpParam = copy.deepcopy(param)
                cpParam.ids = batch
                res.append(cpParam)
        return res
