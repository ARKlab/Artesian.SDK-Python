import copy

from Artesian._Query.QueryParameters.ActualQueryParameters import ActualQueryParameters
from Artesian._Query.QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from Artesian._Query.QueryParameters.AuctionQueryParameters import AuctionQueryParameters
from Artesian._Query.QueryParameters.VersionedQueryParameters import VersionedQueryParameters
from Artesian._Query.QueryParameters.MasQueryParameters import MasQueryParameters
from Artesian._GMEPublicOffers.QueryParameters.GMEPOfferQueryParameters import GMEPOfferQueryParameters

class DefaultPartitionStrategy:
    """
    This class sets the default strategy to partition Query Parameters.

    """
    maxNumberOfIds = 15
    """ Only 15 allowed."""
    
    def PartitionActual(self, actualQueryParameters: list[ActualQueryParameters]) -> list[ActualQueryParameters]:
        """ The partition strategy for the Actual Time Series Query.

            Returns:
                The input list of Actual Time Series Query parameters partitioned with the defined strategy. """
        return self._tsPartitionStrategy(actualQueryParameters)

    def PartitionAuction(self, auctionQueryParameters: list[AuctionQueryParameters]) -> list[AuctionQueryParameters]:
        """ The partition strategy for the Auction Time Series Query.

            Returns:
                The input list of Auction Time Series Query parameters partitioned with the defined strategy. """
        return self._tsPartitionStrategy(auctionQueryParameters)

    def Partitionversioned(self, versionedQueryParameters: list[VersionedQueryParameters]) -> list[VersionedQueryParameters]:
        """ The partition strategy for the Versioned Time Series Query.

            Returns:
                 The input list of Versioned Time Series Query parameters partitioned with the defined strategy."""
        return self._tsPartitionStrategy(versionedQueryParameters)
       

    def PartitionMas(self, masQueryParameters: list[MasQueryParameters]) -> list[MasQueryParameters]:
        """ The partition strategy for the Market Assessment Query.
        
            Returns:
                The input list of Market Assessment Query parameters partitioned with the defined strategy. """
        return self._tsPartitionStrategy(masQueryParameters)

    def PartitionGMEPOffer(self, gmePOfferQueryParameters: list[GMEPOfferQueryParameters]) -> list[GMEPOfferQueryParameters]:
        """ The partition strategy fot the GME Public Offer Query.
        
            Returns:
                The input list of GME Public Offer Query parameters partitioned with the defined strategy.  """
        return gmePOfferQueryParameters

    def _tsPartitionStrategy(self, Parameters):
        res = []
        for param in Parameters:
            if(param.ids is None):
                res.append(param)
                continue
            leng = len(param.ids)
            batches = [param.ids[i:i + DefaultPartitionStrategy.maxNumberOfIds] for i in range(0, leng, DefaultPartitionStrategy.maxNumberOfIds)]
            for batch in batches:
                cpParam = copy.deepcopy(param)
                cpParam.ids = batch
                res.append(cpParam)
        return res 

