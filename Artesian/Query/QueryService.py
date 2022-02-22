from Artesian.Query.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian.Query.ActualQuery import ActualQuery
from Artesian.Query.AuctionQuery import AuctionQuery
from Artesian.Query.VersionedQuery import VersionedQuery
from Artesian.Query.MasQuery import MasQuery
from Artesian.Query.BidAskQuery import BidAskQuery
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
from Artesian._Configuration.ArtesianConfig import ArtesianConfig


from Artesian.Query.DefaultPartitionStrategy import DefaultPartitionStrategy

class QueryService:
    """ 
        QueryService class contains query types to be created.
    
    """
    __queryRoute = "query" 
    __queryVersion = "v1.0"
    def __init__(self, artesianConfig: ArtesianConfig) -> None:
        """ 
            Inits QueryService
        
            Args:
                artesianConfiguration: The Artesian Configuration.
        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__queryBaseurl = self.__config.baseUrl + "/" + self.__queryRoute + "/" + self.__queryVersion
        self.__partitionStrategy = DefaultPartitionStrategy()
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__queryBaseurl ,self.__config.apiKey)
    def createActual(self) -> ActualQuery:
        """ 
            Create Actual Time Serie Query.
        
            Returns:
                Actual Time Serie ActualQuery. 
        """
        return ActualQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createAuction(self) -> AuctionQuery:
        """ 
            Create Auction Time Serie Query.
            
            Returns:
                Auction Time Serie AuctionQuery. 
        """
        return AuctionQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createVersioned(self) -> VersionedQuery:
        """ 
            Create Versioned Time Serie Query.
        
            Returns:
                Versioned Time Serie VersionedQuery. 
        """
        return VersionedQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createMarketAssessment(self) -> MasQuery:
        """ 
            Create Market Assessment Time Serie Query.
        
            Returns:
                Market Assessment Time Serie MasQuery. 
        """
        return MasQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createBidAsk(self) -> BidAskQuery:
        """ 
            Create Bid Ask Time Serie Query.
        
            Returns:
                Bid Ask Time Serie MasQuery.
        """
        return BidAskQuery(self.__client, self.__executor, self.__partitionStrategy)