from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianConfig import ArtesianConfig
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
from Artesian._Services.Dto.PagedResult import PagedResultCurveRangeEntity
from Artesian._Services.Dto.MarketDataEntityInput import MarketDataEntityInput
from Artesian._Services.Dto.MarketDataEntityOutput import MarketDataEntityOutput
import asyncio

from typing import NewType

class MarketDataService:
    """ 
        A MarketData Entity represents a data curve enriched by its metadata.
        Each entity is composed of some fundamental parameters:

    """

    __version = "v2.1"
    def __init__(self, artesianConfig: ArtesianConfig) -> None:
        """ 
            Inits the MarketData Service 
        
            Using the ArtesianServiceConfig, is possible to create an istance of the MarketDataService which is used to retrieve and edit MarketData references.

            Args:
                artesianConfiguration: The Artesian Configuration.

        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__serviceBaseurl = self.__config.baseUrl + "/" + self.__version
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__serviceBaseurl ,self.__config.apiKey)

    async def readCurveRangeAsync(self, id: int, page: int, pageSize: int, 
        product: str=None, versionFrom: str=None, versionTo: str=None) -> PagedResultCurveRangeEntity:
        """
            Reads paged set of available versions of the marketdata by id.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                Paged result of CurveRange entity (Async).
        """

        url = "/marketdata/entity/" + str(id) + "/curves"
        params ={
                  'page':page,
                  'pageSize':pageSize            
                }
        if(versionFrom is not None):            
            params['versionFrom'] = versionFrom
        if(versionTo is not None):
            params['versionTo'] = versionTo
        if(product is not None):
            params['product'] = product       
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, retcls=PagedResultCurveRangeEntity, params=params)])
            return res[0]

    def readCurveRange(self, id: int, page: int, pageSize: int, 
        product: str=None, versionFrom: str=None, versionTo: str=None) -> PagedResultCurveRangeEntity:
        """
            Reads paged set of available versions of the marketdata by id.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                Paged result of CurveRange entity.
        """
        return _get_event_loop().run_until_complete(self.readCurveRangeAsync(id, page, pageSize, product, versionFrom, versionTo))


    async def readMarketDataRegistryByIdAsync(self, id: int) -> MarketDataEntityOutput:
        """
            Reads MarketData by id with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
            
            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None, retcls=MarketDataEntityOutput)])
            return res[0]

    def readMarketDataRegistryById(self, id: int) -> MarketDataEntityOutput :  
        """
            Reads MarketData by curve name with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.

            Returns:
                MarketData Entity Output.
        """ 
        return _get_event_loop().run_until_complete(self.readMarketDataRegistryByIdAsync(id))

    async def updateMarketDataAsync(self, id: int, entity: MarketDataEntityInput) -> MarketDataEntityOutput :
        """ 
            Saves the given MarketData Entity

            Args:
                id: int of the marketdata to be updated
                
            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'PUT', url, entity, MarketDataEntityOutput)])
            return res[0]

    def updateMarketData(self, id: int):
        """ 
            Saves the given MarketData Entity

            Args:
                id: int of the marketdata to be updated

            Returns:
                MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(self.updateMarketDataAsync(id))

    async def deleteMarketDataAsync(self, id: int) -> None :
        """ 
            Delete the specific MarketData entity by id

            Args:
                id: int of the marketdata to be deleted

            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'DELETE', url, None)])
            return res[0]

    def deleteMarketData(self, id: int) -> None :
        """ 
            Delete the specific MarketData entity by id

            Args: 
                id: int of the marketdata to be deleted

            Returns:
                MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(self.deleteMarketDataAsync(id))

    async def readMarketDataRegistryByNameAsync(self, provider: str, curveName: str) -> MarketDataEntityOutput:
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: string of the curve name to be retrieved.

            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity" 
        params = {"provider": provider , "curveName":curveName}
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None, retcls=MarketDataEntityOutput, params = params)])
            return res[0]

    def readMarketDataRegistryByName(self, provider: str, curveName: str) -> MarketDataEntityOutput:
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: string of the curve name to be retrieved.
                
            Returns:
                MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(self.readMarketDataRegistryByNameAsync(provider, curveName))

    async def registerMarketDataAsync(self, entity: MarketDataEntityInput) -> MarketDataEntityOutput:
        """
            Register a new MarketData entity.

            Args:
                entity: The Market Data Entity Input
                
            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity"
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'POST', url, entity, MarketDataEntityOutput)])
            return res[0]

    def registerMarketData(self, entity: MarketDataEntityInput) -> MarketDataEntityOutput:
        """
            Register a new MarketData entity.

            Args:
                entity: The Market Data Entity Input
                
            Returns:
                MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(self.registerMarketDataAsync(id))



def _get_event_loop():
    """
    Wrapper around asyncio get_event_loop.
    Ensures that there is an event loop available.
    An event loop may not be available if the sdk is not run in the main event loop
    """
    try:
        asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    
    return asyncio.get_event_loop()