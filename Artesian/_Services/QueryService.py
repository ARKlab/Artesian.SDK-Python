from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._Query.ActualQuery import _ActualQuery
from Artesian._Query.AuctionQuery import _AuctionQuery
from Artesian._Query.VersionedQuery import _VersionedQuery
from Artesian._Query.MasQuery import _MasQuery
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
class QueryService:
    __queryRoute = "query" 
    __queryVersion = "v1.0"
    def __init__(self, artesianConfig):
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__queryBaseurl = self.__config.baseUrl + "/" + self.__queryRoute + "/" + self.__queryVersion
        self.__partitionStrategy = DefaultPartitionStrategy()
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__queryBaseurl ,self.__config.apiKey)
    def createActual(self):
        return _ActualQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createAuction(self):
        return _AuctionQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createVersioned(self):
        return _VersionedQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createMarketAssessment(self):
        return _MasQuery(self.__client, self.__executor, self.__partitionStrategy)