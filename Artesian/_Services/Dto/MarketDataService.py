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
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()

    # GET /v2.1/marketdata/entity/{id}  -->> REMEMBER TO REMOVE THESE COMMENTS
    # Gets MarketData entity by curve id
    # 1 ASYNC
    async def readMarketDataRegistryAsync(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
        """
            Reads MarketData by curve name with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSeize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                MarketData Entity Output (Async).

        """
        url = "/" + str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        with client as c:
            res = await asyncio.gather(*[c.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()

    # GET /v2.1/marketdata/entity/{id} -->> REMEMBER TO REMOVE
    # 1 NON-ASYNC
    def readMarketDataRegistry(self, id: int, page: int, pageSize: int, product: str=None, versionFrom: str=None, versionTo: str=None):
        """
            Reads MarketData by curve name with MarketDataID.

            Args:
                id: ID of the marketdata to be retrieved.
                page: int of the page number (1-based).
                pageSeize: int of the pagesize.
                product: Market product in the case of Market Assessment.
                versionFrom: String of the start date of version range (ISO format).
                versionTo: String of the end date of version range (ISO format).
            
            Returns:
                MarketData Entity Output.

        """
        url = "/" + str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        with client as c:
            mkdret = c.exec('GET', 'v2.1/marketdata/entity/100086867'
                    MarketDataEntityOutput)
            return mkdret 

    # POST /v2.1/marketdata/entity -->> Register a given MarketData entity
    #5 ??
    #async def registerMarketDataAsync(self, id: int, marketDataEntityInput: MarketDataEntityInput):




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