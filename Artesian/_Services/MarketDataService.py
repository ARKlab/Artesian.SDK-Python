from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian._Configuration.ArtesianPolicyConfig import ArtesianPolicyConfig
import asyncio
import itertools
class MarketDataService:
    __queryRoute = "marketdata/entity" 
    __version = "v2.1"
    def __init__(self, artesianConfig):
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig(None, None, None)
        self.__queryBaseurl = self.__config.baseUrl + "/" + self.__version + "/" + self.__queryRoute 
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__queryBaseurl ,self.__config.apiKey)
    async def readCurveRangeAsync(self, id, page, pageSize, product=None, versionFrom=None, versionTo=None):
        url = "/" + str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()
    def readCurveRange(self, id, page, pageSize, product=None, versionFrom=None, versionTo=None):
        url = str(id) + "/curves?page=" + str(page) + "&pagesize=" + str(pageSize) 
        if(versionFrom is not None and versionTo is not None):
            url = url + "&versionFrom=" + versionFrom + "&versionTo=" + versionTo 
        loop = asyncio.get_event_loop()
        rr = loop.run_until_complete(self.readCurveRangeAsync(id, page, pageSize, product, versionFrom, versionTo))
        return rr
