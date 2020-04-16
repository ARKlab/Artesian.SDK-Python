from Artesian._GMEPublicOffers.QueryParameters.GMEPOfferQueryParameters import GMEPOfferQueryParameters
from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._GMEPublicOffers.Config.GenerationType import GenerationType
from Artesian._GMEPublicOffers.Config.Market import Market
from Artesian._GMEPublicOffers.Config.Purpose import Purpose
from Artesian._GMEPublicOffers.Config.Scope import Scope
from Artesian._GMEPublicOffers.Config.Status import Status
from Artesian._GMEPublicOffers.Config.UnitType import UnitType
from Artesian._GMEPublicOffers.Config.Zone import Zone

import asyncio
import itertools
import urllib

class _GMEPOfferQuery:
    __routePrefix = "extract"
    def __init__(self, client, requestExecutor, partitionStrategy):
        queryParameters = GMEPOfferQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None, None, None, None, None, None, None )
        self._queryParameters = queryParameters
        self.__client = client
        self.__executor = requestExecutor
        self.__partition= partitionStrategy

    def forScope(self, scope):
        self._queryParameters.scope = scope
        return self
    def forStatus(self, status):
        self._queryParameters.status = status
        return self
    def forUnitType(self, unitType):
        self._queryParameters.unitType = unitType
        return self
    def forDate(self, date):
        self._queryParameters.extractionRangeSelectionConfig.date = date
        return self
    def forUnit(self, unit):
        self._queryParameters.unit = unit
        return self
    def forOperator(self, operator):
        self._queryParameters.operator = operator
        return self
    def forZone(self, zone):
        self._queryParameters.zone = zone
        return self
    def forMarket(self, market):
        self._queryParameters.market = market
        return self
    def forPurpose(self, purpose):
        self._queryParameters.purpose = purpose
        return self
    def forBAType(self, baType):
        self._queryParameters.baType = baType
        return self
    def forGenerationType(self, generationType):
        self._queryParameters.baType = generationType
        return self
    def withPagination(self, pagenumber,pagesize):
        self._queryParameters.page = pagenumber
        self._queryParameters.pageSize = pagesize
        return self
    def execute(self):
        url = self.__buildRequest()
        return self._exec(url)
    async def executeAsync(self):
        url = self.__buildRequest()
        return self._execAsync(url)
    def __buildRequest(self):
        self._validateQuery()
        qps = self.__partition.PartitionGMEPOffer([self._queryParameters])
        for qp in qps:
            url = f"/{self.__routePrefix}/{self._buildExtractionRangeRoute(qp)}/{qp.purpose}/{qp.status}?"
            if not (qp.page is None):
                url = url + "page=" + str(qp.page)
            if not (qp.pageSize is None):
                url = url + "&pageSize=" + str(qp.pageSize)        
            if not (qp.scope is None):
                sep = ","
                scope= sep.join(map(str,qp.scope))
                enc = urllib.parse.quote_plus(scope)
                url = url + "&scope=" + enc
            if not (qp.unitType is None):
                sep = ","
                unitType= sep.join(map(str,qp.unitType))
                enc = urllib.parse.quote_plus(unitType)
                url = url + "&unitType=" + enc
            if not (qp.unit is None):
                sep = ","
                unit= sep.join(map(str,qp.unit))
                enc = urllib.parse.quote_plus(unit)
                url = url + "&unit=" + enc
            if not (qp.generationType is None):
                sep = ","
                generationType = sep.join(map(str,qp.generationType))
                enc = urllib.parse.quote_plus(generationType)
                url = url + "&generationType=" + enc
            if not (qp.operator is None):
                sep = ","
                operator= sep.join(map(str,qp.operator))
                enc = urllib.parse.quote_plus(operator)
                url = url + "&operator=" + enc
            if not (qp.zone is None):
                sep = ","
                zone= sep.join(map(str,qp.zone))
                enc = urllib.parse.quote_plus(zone)
                url = url + "&zone=" + enc
            if not (qp.market is None):
                sep = ","
                market= sep.join(map(str,qp.market))
                enc = urllib.parse.quote_plus(market)
                url = url + "&market=" + enc    
            if not (qp.baType is None):
                sep = ","
                baType= sep.join(map(str,qp.baType))
                enc = urllib.parse.quote_plus(baType)
                url = url + "&baType=" + enc         
        return url

    def _buildExtractionRangeRoute(self, queryParamaters):
        subPath = f"{self.__toUrlParam(queryParamaters.extractionRangeSelectionConfig.date)}"
        return subPath
    def _buildExtractionStatus(self, status):
        subPath = f"{urllib.parse.quote_plus(status)}"
        return subPath
    def _buildExtractionPurpose(self, purpose):
        subPath = f"{urllib.parse.quote_plus(purpose)}"
        return subPath
    def _exec(self, url):
        loop = asyncio.get_event_loop()
        rr = loop.run_until_complete(self._execAsync(url))
        return rr
    async def _execAsync(self, url):
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0].json()
    def __toUrlParam(self, date):
        return f"{date}"   
    def _validateQuery(self):
        if(self._queryParameters.scope is not None):
            for x in self._queryParameters.scope:
                res=getattr(Scope, x, None)
                if (res is None):
                    self._raiseError("scope",x)
        if(self._queryParameters.market is not None):
            for x in self._queryParameters.market:
                res=getattr(Market, x, None)
                if (res is None):
                    self._raiseError("Market", x)
        if(self._queryParameters.unitType is not None):
            for x in self._queryParameters.unitType:
                res=getattr(UnitType, x, None)
                if (res is None):
                    self._raiseError("UnitType", x)
        if(self._queryParameters.zone is not None):
            for x in self._queryParameters.zone:
                res=getattr(Zone, x, None)
                if (res is None):
                    self._raiseError("Zone", x)

    
    def _raiseError(self, category, value):
        raise Exception(f"The value {value} is not supported as {category}. Please provide a valid one.")