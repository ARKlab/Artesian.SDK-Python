from Artesian._Configuration.ArtesianConfig import ArtesianConfig
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._GMEPublicOffers.GMEPOfferQuery import _GMEPOfferQuery
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig

class GMEPublicOfferService: 
    """ 
        This class contains GME Public Offer Query types to be created
    
        Attributes:
            artesianConfiguration: The Artesian Configuration.
    """
    __offerstype = "gmepublicoffer"
    __version = "v1.0"
    def __init__(self, artesianConfig: ArtesianConfig):
        """ 
            Inits for GME Public Offer Service.

            Args:
                Artesian Configuration.
        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__queryBaseurl = self.__config.baseUrl + "/" + self.__offerstype + "/" + self.__version 
        self.__partitionStrategy = DefaultPartitionStrategy()
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__queryBaseurl ,self.__config.apiKey)
    def createQuery(self) -> _GMEPOfferQuery:
        """ Creates GME Public Offer Query."""
        return _GMEPOfferQuery(self.__client, self.__executor, self.__partitionStrategy)