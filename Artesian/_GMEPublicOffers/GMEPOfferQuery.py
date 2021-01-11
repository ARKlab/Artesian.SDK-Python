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
from Artesian._GMEPublicOffers.Config.BaType import BaType

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
            url = f"/{self.__routePrefix}/{self._buildExtractionRangeRoute(qp)}/{self.__getPurpose(qp.purpose)}/{self.__getStatus(qp.status)}?"
            if not (qp.page is None):
                url = url + "page=" + str(qp.page)
            if not (qp.pageSize is None):
                url = url + "&pageSize=" + str(qp.pageSize)        
            if not (qp.scope is None):
                sep = ","
                scope= sep.join(map(lambda x:self.__getScope(x),qp.scope))
                enc = urllib.parse.quote_plus(scope)
                url = url + "&scope=" + enc
            if not (qp.unitType is None):
                sep = ","
                unitType= sep.join(map(lambda x:self.__getUnitType(x),qp.unitType))
                enc = urllib.parse.quote_plus(unitType)
                url = url + "&unitType=" + enc
            if not (qp.unit is None):
                sep = ","
                unit= sep.join(map(str,qp.unit))
                enc = urllib.parse.quote_plus(unit)
                url = url + "&unit=" + enc
            if not (qp.generationType is None):
                sep = ","
                generationType = sep.join(map(lambda x:self.__getGenerationType(x),qp.generationType))
                enc = urllib.parse.quote_plus(generationType)
                url = url + "&generationType=" + enc
            if not (qp.operator is None):
                sep = ","
                operator= sep.join(map(str,qp.operator))
                enc = urllib.parse.quote_plus(operator)
                url = url + "&operator=" + enc
            if not (qp.zone is None):
                sep = ","
                zone= sep.join(map(lambda x:self.__getZone(x),qp.zone))
                enc = urllib.parse.quote_plus(zone)
                url = url + "&zone=" + enc
            if not (qp.market is None):
                sep = ","
                market= sep.join(map(lambda x:self.__getMarket(x),qp.market))
                enc = urllib.parse.quote_plus(market)
                url = url + "&market=" + enc    
            if not (qp.baType is None):
                sep = ","
                baType= sep.join(map(lambda x:self.__getBaType(x),qp.baType))
                enc = urllib.parse.quote_plus(baType)
                url = url + "&baType=" + enc         
        return url

    def __getScope(self,scope):
        switcher = {
            Scope.ACC: "ACC", 
            Scope.AS: "AS",
            Scope.CA: "CA",
            Scope.GR1: "GR1", 
            Scope.GR2: "GR2",
            Scope.GR3: "GR3", 
            Scope.GR4: "GR4", 
            Scope.RS: "RS"
        }
        vr = switcher.get(scope, "DefScope")
        if vr == "DefScope" :
            raise Exception("Not supported Scope")
        return vr
    def __getGenerationType(self,generationType):
        switcher = {
            GenerationType.AUTOGENERATION: "AUTOGENERATION", 
            GenerationType.BIOMASS: "BIOMASS",
            GenerationType.COAL: "COAL",
            GenerationType.GAS: "GAS", 
            GenerationType.GASOIL: "GASOIL",
            GenerationType.HYDRO: "HYDRO", 
            GenerationType.MIXED: "MIXED", 
            GenerationType.OIL: "RS",
            GenerationType.OTHER: "OTHER", 
            GenerationType.PV: "PV",
            GenerationType.THERMAL: "THERMAL", 
            GenerationType.WIND: "WIND"
        }
        vr = switcher.get(generationType, "DefGen")
        if vr == "DefGen" :
            raise Exception("Not supported GeneratioType")
        return vr
    def __getMarket(self,market):
        switcher = {
            Market.MGP: "MGP", 
            Market.MSD: "MSD",
            Market.MI1: "MI1",
            Market.MI2: "MI2",
            Market.MI3: "MI3",
            Market.MI4: "MI4",
            Market.MI5: "MI5",
            Market.MI6: "MI6",
            Market.MI7: "MI7",
            Market.MB: "MB",
            Market.MB2: "MB2",
            Market.MB3: "MB3",
            Market.MB4: "MB4",
            Market.MB5: "MB5",
            Market.MB6: "MB6"
        }
        vr = switcher.get(market, "DefMarket")
        if vr == "DefMarket" :
            raise Exception("Not supported Market")
        return vr
    def __getPurpose(self,purpose):
        switcher = {
            Purpose.BID: "BID", 
            Purpose.OFF: "OFF"
        }
        vr = switcher.get(purpose, "Defpurp")
        if vr == "Defpurp" :
            raise Exception("Not supported Purpose")
        return vr
    def __getStatus(self,status):
        switcher = {
            Status.ACC: "ACC", 
            Status.INC: "INC",
            Status.REJ: "REJ",
            Status.REP: "REP",
            Status.REV: "REV",
            Status.SUB: "SUB"
        }
        vr = switcher.get(status, "DefStatus")
        if vr == "DefStatus" :
            raise Exception("Not supported Status")
        return vr    
    def __getUnitType(self,unitType):
        switcher = {
            UnitType.UP: "UP", 
            UnitType.UC: "UC",
            UnitType.UPV: "UPV",
            UnitType.UCV: "UCV"
        }
        vr = switcher.get(unitType, "DefunitType")
        if vr == "DefunitType" :
            raise Exception("Not supported Unit Type")
        return vr
    def __getBaType(self,baType):
        switcher = {
            BaType.NULL: "NULL", 
            BaType.NREV: "NREV",
            BaType.REV: "REV",
            BaType.NETT: "NETT"
        }
        vr = switcher.get(baType, "DefbaType")
        if vr == "DefbaType" :
            raise Exception("Not supported BaType")
        return vr
    def __getZone(self,zone):
        switcher = {
            Zone.AUST: "AUST", 
            Zone.BRNN: "BRNN",
            Zone.CNOR: "CNOR",
            Zone.COAC: "COAC",
            Zone.CORS: "CORS",
            Zone.CSUD: "CSUD",
            Zone.FOGN: "FOGN",
            Zone.FRAN: "FRAN",
            Zone.GREC: "GREC",
            Zone.MALT: "MALT",
            Zone.NORD: "NORD",
            Zone.PRGP: "PRGP",
            Zone.ROSN: "ROSN",
            Zone.SARD: "SARD",
            Zone.SICI: "SICI",
            Zone.SLOV: "SLOV",
            Zone.SUD: "SUD",
            Zone.SVIZ: "SVIZ",
            Zone.CALA: "CALA"
        }
        vr = switcher.get(zone, "DefZone")
        if vr == "DefZone" :
            raise Exception("Not supported Zone")
        return vr   
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
        if(self._queryParameters.purpose is None):
            raise Exception("Extraction Purpose must be provided. Use .forScope() argument takes a scope type")
        if(self._queryParameters.extractionRangeSelectionConfig.date is None):
            raise Exception("Extraction Date must be provided. Use .forDate() argument takes a string formatted as YYYY-MM-DD")
        if(self._queryParameters.status is None):
            raise Exception("Extraction Status must be provided. Use .forStatus() argument takes a status type")