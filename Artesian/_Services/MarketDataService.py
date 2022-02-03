from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianConfig import ArtesianConfig
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
from Artesian._Services.Dto.MarketDataEntityInput import MarketDataEntityInput
from Artesian._Services.Dto.MarketDataEntityOutput import MarketDataEntityOutput
import asyncio

class MarketDataService:
    """ Class for the Market Data Service. """
    __version = "v2.1"
    def __init__(self, artesianConfig: ArtesianConfig) -> None:
        """ 
            Inits for the Market Data Service. 
            
            Args: 
                artesianConfig: The Artesian COnfiguration.
        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__serviceBaseurl = self.__config.baseUrl + "/" + self.__version
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__serviceBaseurl ,self.__config.apiKey)

# GET /marketdata/entity/{id}/curves  -->> REMEMBER TO REMOVE THESE COMMENTS
# Gets all the metadata versions by id
    async def readCurveRangeAsync(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
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

        url = "/marketdata/entity/" + str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None):
            url = url + "&versionFrom=" + versionFrom
        if(versionTo is not None):
            url = url + "&versionTo=" + versionTo 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0]

 # GET /v2.1/marketdata/entity/{id}/curves  -->> REMEMBER TO REMOVE THESE COMMENTS
 # Gets all the metadata versions by id
    def readCurveRange(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
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
        return asyncio.get_event_loop().run_until_complete(self.readCurveRangeAsync(id, page, pageSize, product, versionFrom, versionTo))


    # 1 ASYNC
    # GET /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Gets MarketData entity by curve id
    async def readMarketDataRegistryAsync(self, id: int):
        """
            Reads MarketData by id with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
            
            Returns:
                MarketData Entity Output (Async).

        """
        url = "/" + str(id) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None, retcls=MarketDataEntityOutput)])
            return res[0]

    # 1 NON-ASYNC
    # GET /v2.1/marketdata/entity/{id} -->> REMEMBER TO REMOVE
    def readMarketDataRegistry(self, id: int):
        """
            Reads MarketData by curve name with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
                X-Artesian-Agent
            Returns:
                MarketData Entity Output.

        """        
        return asyncio.get_event_loop().run_until_complete(self.readMarketDataRegistryAsync(id))

    # 2 ASYNC
    # PUT /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Save the MarketData by given entity
    async def updateMarketDataAsync(self, entity: MarketDataEntityInput):
        """ 
            Updates the given MarketData Entity

            Args:
                id: int of the marketdata to be updated
                
            Returns:
                MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(entity.marketDataId) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'PUT', url, entity, MarketDataEntityOutput)])
            return res[0]

    # 2 NON-ASYNC
    # PUT /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Save the MarketData by given entity
    def updateMarketData(self, id: int, ):
        """ 
            Updates the given MarketData Entity

            Args:
                id: int of the marketdata to be updated

            Returns:
                MarketData Entity Output.
        """
        return asyncio.get_event_loop().run_until_complete(self.updateMarketDataAsync(id))

    # 3 ASYNC
    # DELETE /v2.1/marketdata/entity/{id} -->> REMEMBER TO REMOVE
    # Delete MarketData entity by id
    async def deleteMarketDataAsync(self, id: int, ):
        """ 
            Delete the specific MarketData entity by id

            Args:
                id: int of the marketdata to be deleted

            Returns:
                MarketData Entity Output.
        """
        url = "/" + str(id) 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'DELETE', url, None)])
            return res[0].json()

    # 3 NON-ASYNC	
    # DELETE /v2.1/marketdata/entity/{id} -->> REMEMBER TO REMOVE
    # Delete MarketData entity by id
    def deleteMarketData(self, id: int, ):
        """ 
            Delete the specific MarketData entity by id

            Args:
                id: int of the marketdata to be deleted

            Returns:
                MarketData Entity Output.
        """
        return asyncio.get_event_loop().run_until_complete(self.deleteMarketDataAsync(id))
    # 4 ASYNC
    # GET /v2.1/marketdata/entity
    # Gets MarketData entity by provider and curveName
    async def readMarketDataRegistryByNameAsync(self, provider: str, curveName: str):
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: strinf of the curve name to be retrieved.

            Returns:
                MarketData Entity Output (Async).

        """
        url = "/marketdata/entity?provider=" + str(provider) + "&curveName=" + str(curveName)
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None, retcls=MarketDataEntityOutput)])
            return res[0]

    # 4 NON-ASYNC
    # GET /v2.1/marketdata/entity
    # Gets MarketData entity by provider and curveName
    def readMarketDataRegistryByName(self, provider: str, curveName: str):
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: strinf of the curve name to be retrieved.
                
            Returns:
                MarketData Entity Output.

        """
        return asyncio.get_event_loop().run_until_complete(self.readMarketDataRegistryByNameAsync(provider, curveName))

    
    # POST ASYNC
    async def postMarketDataAsync(self, entity: MarketDataEntityInput):
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

    # POST NON-ASYNC
    def postMarketData(self, entity: MarketDataEntityInput):
        """
            Register a new MarketData entity.

            Args:
                entity: The Market Data Entity Input
                
            Returns:
                MarketData Entity Output.
        """
        return asyncio.get_event_loop().run_until_complete(self.postMarketDataAsync(id))

def get_event_loop():
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