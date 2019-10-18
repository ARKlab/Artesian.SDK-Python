from Artesian._GMEPublicOffers.QueryParameters.GMEPOfferQueryParameters import GMEPOfferQueryParameters
from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Configuration.DefaultPartitionStrategy import DefaultPartitionStrategy
from Artesian._GMEPublicOffers.Config.ExtractionRangeType import ExtractionRangeType
from Artesian._GMEPublicOffers.Config.GroupedBy import GroupedBy
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
    def __init__(self, client, requestExecutor, partitionStrategy):
        queryParameters = GMEPOfferQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None, None, None, None, None) 
        self._queryParameters = queryParameters
        self._client = client
        self._requestExecutor = requestExecutor
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
    def inAbsoluteDateRange(self, start, end):
        self._queryParameters.extractionRangeType = ExtractionRangeType.DATE_RANGE
        self._queryParameters.extractionRangeSelectionConfig.dateStart = start
        self._queryParameters.extractionRangeSelectionConfig.dateEnd = end
        return self
    def isPivoted(self, pivot):
        self._queryParameters.pivot = pivot
        return self
    def forUnit(self, unit):
        self._queryParameters.unit = unit
        return self
    def isGroupedBy(self, groupby):
        self._queryParameters.groupby = groupby
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
    def execute(self):
        urls = self.__buildRequest()
        return self._exec(urls)
    async def executeAsync(self):
        urls = self.__buildRequest()
        return self._execAsync(urls)
    def __buildRequest(self):
        self._validateQuery()
        qps = self.__partition.PartitionGMEPOffer([self._queryParameters])
        urls = []
        for qp in qps:
            url = f"?{self._buildExtractionRangeRoute(qp)}"
            if not (qp.scope is None):
                sep = ","
                scope= sep.join(map(str,qp.scope))
                enc = urllib.parse.quote_plus(scope)
                url = url + "&scope=" + enc
            if not (qp.status is None):
                sep = ","
                status= sep.join(map(str,qp.status))
                enc = urllib.parse.quote_plus(status)
                url = url + "&status=" + enc
            if not (qp.unitType is None):
                sep = ","
                unitType= sep.join(map(str,qp.unitType))
                enc = urllib.parse.quote_plus(unitType)
                url = url + "&unitType=" + enc
            if not (qp.status is None):
                sep = ","
                status= sep.join(map(str,qp.status))
                enc = urllib.parse.quote_plus(status)
                url = url + "&status=" + enc
            if not (qp.pivot is None):
                url = url + "&pivot=" + str(qp.pivot)
            if not (qp.unit is None):
                sep = ","
                unit= sep.join(map(str,qp.unit))
                enc = urllib.parse.quote_plus(unit)
                url = url + "&unit=" + enc
            if not (qp.groupby is None):
                sep = ","
                groupby= sep.join(map(str,qp.groupby))
                enc = urllib.parse.quote_plus(groupby)
                url = url + "&groupby=" + enc
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
            if not (qp.purpose is None):
                sep = ","
                purpose= sep.join(map(str,qp.purpose))
                enc = urllib.parse.quote_plus(purpose)
                url = url + "&purpose=" + enc
            
            urls.append(url)
        return urls

    def _buildExtractionRangeRoute(self, queryParamaters):
        subPath = f"{self.__toUrlParam(queryParamaters.extractionRangeSelectionConfig.dateStart, queryParamaters.extractionRangeSelectionConfig.dateEnd)}"
        return subPath
    def _exec(self, urls):
        loop = asyncio.get_event_loop()
        rr = loop.run_until_complete(self._execAsync(urls))
        return rr
    async def _execAsync(self, urls):
            with self._client as c:
                res = await asyncio.gather(*[self._requestExecutor.exec(c.exec, 'GET', i, None) for i in urls])
                return list(itertools.chain(*map(lambda r: r.json(),res)))
    def __toUrlParam(self, start, end):
        return f"Start={start}&End={end}"
    def _validateQuery(self):
        if(self._queryParameters.extractionRangeType is None):
            raise Exception("Data extraction range must be provided. Provide a date range , period or period range or an interval eg .InAbsoluteDateRange()")
        if(self._queryParameters.scope is not None):
            for x in self._queryParameters.scope:
                res=getattr(Scope, x, None)
                if (res is None):
                    self._raiseError("scope",x)
        if(self._queryParameters.groupby is not None):
            for x in self._queryParameters.groupby:
                res=getattr(GroupedBy, x, None)
                if (res is None):
                    self._raiseError("groupby", x)
        if(self._queryParameters.market is not None):
            for x in self._queryParameters.market:
                res=getattr(Market, x, None)
                if (res is None):
                    self._raiseError("Market", x)
        if(self._queryParameters.pivot is not None):
            if(str(self._queryParameters.pivot) != "True" and str(self._queryParameters.pivot) != "False"):
                self._raiseError("Pivot", str(self._queryParameters.pivot))
        if(self._queryParameters.purpose is not None):
            for x in self._queryParameters.purpose:
                res=getattr(Purpose, x, None)
                if (res is None):
                    self._raiseError("Purpose", x)
        if(self._queryParameters.status is not None):
            for x in self._queryParameters.status:
                res=getattr(Status, x, None)
                if (res is None):
                    self._raiseError("Status", x)
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