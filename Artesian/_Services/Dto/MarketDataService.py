from http import client
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianConfig import ArtesianConfig
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
import asyncio

from Artesian._Services.Dto.MarketDataEntityInput import MarketDataEntityInput
class MarketDataService:
    """ 
        Class for the Market Data Service.
        
        Attributes:
            artesianConfig: The Artesian Configuration.
    """
    __queryRoute = "marketdata/entity" 
    __version = "v2.1"
    def __init__(self, artesianConfig: ArtesianConfig) -> None:
        """ 
            Inits for the Market Data Service. 
            
            Args: 
                artesianConfig: The Artesian COnfiguration.
        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__queryBaseurl = self.__config.baseUrl + "/" + self.__version + "/" + self.__queryRoute 
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__queryBaseurl ,self.__config.apiKey)

# GET /v2.1/marketdata/entity/{id}/curves  -->> REMEMBER TO REMOVE THESE COMMENTS
# Gets all the metadata versions by id
    async def readCurveRangeAsync(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
        """
            Reads paged set of available versions of the marketdata by id.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSeize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                Paged result of CurveRange entity (Async).
        """

        url = "/" + str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        with self.__client as c:
            res = await asyncio.gather(* .exec(c.exec, 'GET', url, None)])
            return res[0].json()

 # GET /v2.1/marketdata/entity/{id}/curves  -->> REMEMBER TO REMOVE THESE COMMENTS
 # Gets all the metadata versions by id
    def readCurveRange(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
        """
            Reads paged set of available versions of the marketdata by id.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSeize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                Paged result of CurveRange entity.
        """
        url = str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        loop = asyncio.get_event_loop()
        rr = loop.run_until_complete(self.readCurveRangeAsync(id, page, pageSize, product, versionFrom, versionTo))
        return rr


    # 1 ASYNC
    # GET /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Gets MarketData entity by curve id
    async def readMarketDataRegistryAsync(self, id: int, ):
        """
            Reads MarketData by id with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
            
            Returns:
                MarketData Entity Output (Async).

        """
        url = "/" + str(id) 
        with client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()

    # 1 NON-ASYNC
    # GET /v2.1/marketdata/entity/{id} -->> REMEMBER TO REMOVE
    def readMarketDataRegistry(self, id: int,  ):
        """
            Reads MarketData by curve name with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
                X-Artesian-Agent
            Returns:
                MarketData Entity Output.

        """
        url = str(id)
        url = url
        loop = get_event_loop()
        rr = loop.run_until_complete(self.readMarketDataRegistryAsync(id))
        return rr

    # 2 ASYNC
    # PUT /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Save the MarketData by given entity
    async def updateMarketDataAsync(self, id: int, ):
        """ 
            Updates the given MarketData Entity

            Args:
                id: int of the marketdata to be updated
                
            Returns:
                MarketData Entity Output (Async).
        """
        url = "/" + str(id) 
        with client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'PUT', url, None)])
            return res[0].json()

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
        url = str(id)
        url = url
        loop = get_event_loop()
        rr = loop.run_until_complete(self.updateMarketDataAsync(id))
        return rr

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
        with client as c:
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
        url = str(id)
        url = url
        loop = get_event_loop()
        rr = loop.run_until_complete(self.deleteMarketDataAsync(id))
        return rr
    # 4 ASYNC
    # GET /v2.1/marketdata/entity
    # Gets MarketData entity by provider and curveName
    async def ReadMarketDataRegistryAsync(self, provider: str, curveName: str):
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: strinf of the curve name to be retrieved.

            Returns:
                MarketData Entity Output (Async).

        """
        url = "/" + str(provider) + "/curves?name=" + str(curveName)
        if(provider is not None and curveName is not None):
            url = url + "&provider=" + provider + "&curveName=" + curveName
        with client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()
    # 4 NON-ASYNC
    # GET /v2.1/marketdata/entity
    # Gets MarketData entity by provider and curveName
    def ReadMarketDataRegistry(self, provider: str, curveName: str):
        """
            Reads MarketData by provider and curve name.

            Args:
                provider: string of the provider to be retrieved.
                curveName: strinf of the curve name to be retrieved.
                
            Returns:
                MarketData Entity Output.

        """
        url = str(provider) + "/curves?name=" + str(curveName)
        if(provider is not None and curveName is not None):
            url = url + "&provider=" + provider + "&curveName=" + curveName
        url = url
        loop = get_event_loop()
        rr = loop.run_until_complete(self.ReadMarketDataRegistryAsync(provider, curveName))
        return rr

    #5 ASYNC
    # POST /v2.1/marketdata/entity -->> Register a given MarketData entity
    #async def registerMarketDataAsync(self, id: int, marketDataEntityInput: MarketDataEntityInput):
    #REQUEST BODY


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