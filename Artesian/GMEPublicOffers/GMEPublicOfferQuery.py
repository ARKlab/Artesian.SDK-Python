
from __future__ import annotations
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian.GMEPublicOffers.GMEPublicOfferQueryParameters import _GMEPublicOfferQueryParameters
from Artesian.GMEPublicOffers.ExtractionRangeConfig import ExtractionRangeConfig
from ._Enum import GenerationType,Market,Purpose,Scope,Status,UnitType,Zone,BaType
import asyncio
import urllib

class GMEPublicOfferQuery:
    __routePrefix = "extract"
    def __init__(self, client: _Client , 
                       requestExecutor: _RequestExecutor) -> None: 
        """ Inits _GME Public Offer Query """

        queryParameters = _GMEPublicOfferQueryParameters(None,ExtractionRangeConfig(), None, None, None, None, None, None, None, None, None, None, None )
        self._queryParameters = queryParameters
        self.__client = client
        self.__executor = requestExecutor
    def withPagination(self, pagenumber: int, pagesize: int) -> GMEPublicOfferQuery:
        """ 
            Set the request pagination.

            Args:
                pagenumber: int for the GME Public Offer pagenumber to be queried. The pagenumber is (1-based).
                pagesize: int for the GME Public Offer pagesize to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.page = pagenumber
        self._queryParameters.pageSize = pagesize
        return self
    def forScope(self, scope: Scope) -> GMEPublicOfferQuery:
        """ 
            Set the scopes to be queried.

            Args:
                scope: Enum for the GME Public Offer scope to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.scope = scope 
        return self
    def forStatus(self, status: Status) -> GMEPublicOfferQuery:
        """ 
            Set the status to be queried.

            Args:
                status: Enum for the GME Public Offer status to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.status = status
        return self
    def forUnitType(self, unitType: UnitType) -> GMEPublicOfferQuery:
        """ 
            Set the unit types to be queried.

            Args: 
                unitType: Enum for the GME Public Offer Unit Type to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.unitType = unitType
        return self
    def forDate(self, date: str) -> GMEPublicOfferQuery:
        """ 
            Set the date to be queried.

            Args:
                date: string for the date in (ISO format) for the GME Public Offer to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.extractionRangeSelectionConfig.date = date
        return self
    def forUnit(self, unit: str) -> GMEPublicOfferQuery:
        """ 
            Set the units to be queried.
            
            Args:
                unit: string fot the GME Public Offer unit to be queried. 

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.unit = unit
        return self
    def forOperator(self, operator: str) -> GMEPublicOfferQuery:
        """ 
            Set the operators to be queried.
            
            Args:
                operator: string for the GME Public Offer operator to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.operator = operator
        return self
    def forZone(self, zone: Zone) -> GMEPublicOfferQuery:
        """ 
            Set the zones to be queried.

            Args:
                zone: Enum for the GME Public Offer zone to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.zone = zone
        return self
    def forMarket(self, market: Market) -> GMEPublicOfferQuery:
        """ 
            Set the markets to be queried.

            Args:
                market: Enum for the GME Public Offer market to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.market = market
        return self
    def forPurpose(self, purpose: Purpose) -> GMEPublicOfferQuery:
        """ 
            Set the Purpose to be queried.

            Args:
                purpose: Enum for the GME Public Offer purpose to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.purpose = purpose
        return self
    def forBAType(self, baType: BaType) -> GMEPublicOfferQuery:
        """ 
            Set the BATypes to be queried.

            Args:
                baType: Enum for the GME Public Offer baType to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.baType = baType
        return self
    def forGenerationType(self, generationType: GenerationType) -> GMEPublicOfferQuery:
        """ 
            Set the generation types to be queried.

            Args:
                generationType: Enum for the GME Public Offer generation type to be queried.

            Returns:
                GMEPublicOfferQuery.
        """
        self._queryParameters.generationType = generationType
        return self
    def execute(self) -> GMEPublicOfferQuery:
        """ 
            Execute GME Public Offer Query.
        
            Returns:
                GMEPublicOfferQuery.
        """
        url = self.__buildRequest()
        return self._exec(url)
    def executeAsync(self) -> GMEPublicOfferQuery:
        """ 
            Execute GME Public Offer Query.
        
            Returns:
                Enumerable of TimeSerieRow Actual.
        """
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
        loop = get_event_loop()
        rr = loop.run_until_complete(self._execAsync(url))
        return rr
    async def _execAsync(self, url):
        with self.__client as c:
            res = await asyncio.gather(*[self.__executor.exec(c.exec, 'GET', url, None)])
            return res[0]
    def __toUrlParam(self, date):
        return f"{date}"   
    def _validateQuery(self):
        if(self._queryParameters.purpose is None):
            raise Exception("Extraction Purpose must be provided. Use .forScope() argument takes a scope type")
        if(self._queryParameters.extractionRangeSelectionConfig.date is None):
            raise Exception("Extraction Date must be provided. Use .forDate() argument takes a string formatted as YYYY-MM-DD")
        if(self._queryParameters.status is None):
            raise Exception("Extraction Status must be provided. Use .forStatus() argument takes a status type")


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