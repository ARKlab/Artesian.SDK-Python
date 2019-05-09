from Query.DefaultPartitionStrategy import DefaultPartitionStrategy
from Query.ActualQuery import _ActualQuery
from Query.VersionedQuery import _VersionedQuery
from Query.MasQuery import _MasQuery
from ClientsExecutor.RequestExecutor import _RequestExecutor
from ClientsExecutor.Client import _Client
from Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
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
    def createVersioned(self):
        return _VersionedQuery(self.__client, self.__executor, self.__partitionStrategy)
    def createMarketAssessment(self):
        return _MasQuery(self.__client, self.__executor, self.__partitionStrategy)