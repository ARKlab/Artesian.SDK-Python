from __future__ import annotations
from typing import Any, List
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from Artesian.GMEPublicOffers.GMEPublicOfferQueryParameters import (
    _GMEPublicOfferQueryParameters,
)
from ._Enum.BaType import BaType
from ._Enum.GenerationType import GenerationType
from ._Enum.Market import Market
from ._Enum.Purpose import Purpose
from ._Enum.Scope import Scope
from ._Enum.Status import Status
from ._Enum.UnitType import UnitType
from ._Enum.Zone import Zone
import asyncio
from urllib import parse


class GMEPublicOfferQuery:
    __routePrefix = "extract"

    def __init__(
        self: GMEPublicOfferQuery, client: _Client, requestExecutor: _RequestExecutor
    ) -> None:
        """Inits _GME Public Offer Query"""

        queryParameters = _GMEPublicOfferQueryParameters()
        self._queryParameters = queryParameters
        self.__client = client
        self.__executor = requestExecutor

    def withPagination(
        self: GMEPublicOfferQuery, pagenumber: int, pagesize: int
    ) -> GMEPublicOfferQuery:
        """
        Set the request pagination.

        Args:
            pagenumber: int for the GME Public Offer pagenumber to be queried.
                        The pagenumber is (1-based).
            pagesize: int for the GME Public Offer pagesize to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.page = pagenumber
        self._queryParameters.pageSize = pagesize
        return self

    def forScope(self: GMEPublicOfferQuery, scope: List[Scope]) -> GMEPublicOfferQuery:
        """
        Set the scopes to be queried.

        Args:
            scope: Enum for the GME Public Offer scope to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.scope = scope
        return self

    def forStatus(self: GMEPublicOfferQuery, status: Status) -> GMEPublicOfferQuery:
        """
        Set the status to be queried.

        Args:
            status: Enum for the GME Public Offer status to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.status = status
        return self

    def forUnitType(
        self: GMEPublicOfferQuery, unitType: List[UnitType]
    ) -> GMEPublicOfferQuery:
        """
        Set the unit types to be queried.

        Args:
            unitType: Enum for the GME Public Offer Unit Type to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.unitType = unitType
        return self

    def forDate(self: GMEPublicOfferQuery, date: str) -> GMEPublicOfferQuery:
        """
        Set the date to be queried.

        Args:
            date: string for the date in (ISO format) for the Offer to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.extractionRangeConfig.date = date
        return self

    def forUnit(self: GMEPublicOfferQuery, unit: List[str]) -> GMEPublicOfferQuery:
        """
        Set the units to be queried.

        Args:
            unit: string fot the GME Public Offer unit to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.unit = unit
        return self

    def forOperators(
        self: GMEPublicOfferQuery, operators: List[str]
    ) -> GMEPublicOfferQuery:
        """
        Set the operators to be queried.

        Args:
            operators: string for the GME Public Offer operators to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.operators = operators
        return self

    def forZone(self: GMEPublicOfferQuery, zone: List[Zone]) -> GMEPublicOfferQuery:
        """
        Set the zones to be queried.

        Args:
            zone: Enum for the GME Public Offer zone to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.zone = zone
        return self

    def forMarket(
        self: GMEPublicOfferQuery, market: List[Market]
    ) -> GMEPublicOfferQuery:
        """
        Set the markets to be queried.

        Args:
            market: Enum for the GME Public Offer market to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.market = market
        return self

    def forPurpose(self: GMEPublicOfferQuery, purpose: Purpose) -> GMEPublicOfferQuery:
        """
        Set the Purpose to be queried.

        Args:
            purpose: Enum for the GME Public Offer purpose to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.purpose = purpose
        return self

    def forBAType(
        self: GMEPublicOfferQuery, baType: List[BaType]
    ) -> GMEPublicOfferQuery:
        """
        Set the BATypes to be queried.

        Args:
            baType: Enum for the GME Public Offer baType to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.baType = baType
        return self

    def forGenerationType(
        self: GMEPublicOfferQuery, generationType: List[GenerationType]
    ) -> GMEPublicOfferQuery:
        """
        Set the generation types to be queried.

        Args:
            generationType: Enum for the GME Public Offer generation type to be queried.

        Returns:
            GMEPublicOfferQuery.
        """
        self._queryParameters.generationType = generationType
        return self

    def execute(self: GMEPublicOfferQuery) -> Any:
        """
        Execute GME Public Offer Query.

        Returns:
            list of GMEPublicOffers.
        """
        url = self.__buildRequest()
        return self._exec(url)

    async def executeAsync(self: GMEPublicOfferQuery) -> Any:
        """
        Execute GME Public Offer Query.

        Returns:
            Enumerable of TimeSerieRow Actual.
        """
        url = self.__buildRequest()
        return await self._execAsync(url)

    def __buildRequest(self: GMEPublicOfferQuery) -> str:
        self._validateQuery()
        qp = self._queryParameters

        url = "/{0}/{1}/{2}/{3}?_=1".format(
            self.__routePrefix,
            self._buildExtractionRangeRoute(qp),
            self.__getPurpose(qp.purpose),
            self.__getStatus(qp.status),
        )

        if not (qp.page is None):
            url = url + "&page=" + str(qp.page)
        if not (qp.pageSize is None):
            url = url + "&pageSize=" + str(qp.pageSize)
        if not (qp.scope is None):
            sep = ","
            scope = sep.join(map(lambda x: self.__getScope(x), qp.scope))
            enc = parse.quote_plus(scope)
            url = url + "&scope=" + enc
        if not (qp.unitType is None):
            sep = ","
            unitType = sep.join(map(lambda x: self.__getUnitType(x), qp.unitType))
            enc = parse.quote_plus(unitType)
            url = url + "&unitType=" + enc
        if not (qp.unit is None):
            sep = ","
            unit = sep.join(map(str, qp.unit))
            enc = parse.quote_plus(unit)
            url = url + "&unit=" + enc
        if not (qp.generationType is None):
            sep = ","
            generationType = sep.join(
                map(lambda x: self.__getGenerationType(x), qp.generationType)
            )
            enc = parse.quote_plus(generationType)
            url = url + "&generationType=" + enc
        if not (qp.operators is None):
            sep = ","
            operators = sep.join(map(str, qp.operators))
            enc = parse.quote_plus(operators)
            url = url + "&operators=" + enc
        if not (qp.zone is None):
            sep = ","
            zone = sep.join(map(lambda x: self.__getZone(x), qp.zone))
            enc = parse.quote_plus(zone)
            url = url + "&zone=" + enc
        if not (qp.market is None):
            sep = ","
            market = sep.join(map(lambda x: self.__getMarket(x), qp.market))
            enc = parse.quote_plus(market)
            url = url + "&market=" + enc
        if not (qp.baType is None):
            sep = ","
            baType = sep.join(map(lambda x: self.__getBaType(x), qp.baType))
            enc = parse.quote_plus(baType)
            url = url + "&baType=" + enc

        return url

    def __getScope(self: GMEPublicOfferQuery, scope: Scope) -> str:
        switcher = {
            Scope.ACC: "ACC",
            Scope.AS: "AS",
            Scope.CA: "CA",
            Scope.GR1: "GR1",
            Scope.GR2: "GR2",
            Scope.GR3: "GR3",
            Scope.GR4: "GR4",
            Scope.RS: "RS",
        }
        vr = switcher.get(scope, "DefScope")
        if vr == "DefScope":
            raise Exception("Not supported Scope")
        return vr

    def __getGenerationType(
        self: GMEPublicOfferQuery, generationType: GenerationType
    ) -> str:
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
            GenerationType.WIND: "WIND",
        }
        vr = switcher.get(generationType, "DefGen")
        if vr == "DefGen":
            raise Exception("Not supported GeneratioType")
        return vr

    def __getMarket(self: GMEPublicOfferQuery, market: Market) -> str:
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
            Market.MB6: "MB6",
            Market.MBh: "MBh",
            Market.MRR: "MRR",
            Market.MIXBID: "MIXBID",
            Market.MIA1: "MIA1",
            Market.MIA2: "MIA2",
            Market.MIA3: "MIA3",
            Market.MRR: "MRR",
            Market.AFRR: "AFRR",
        }
        vr = switcher.get(market, "DefMarket")
        if vr == "DefMarket":
            raise Exception("Not supported Market")
        return vr

    def __getPurpose(self: GMEPublicOfferQuery, purpose: Purpose | None) -> str:
        if purpose is None:
            raise Exception("Not supported Purpose")
        switcher = {Purpose.BID: "BID", Purpose.OFF: "OFF"}
        vr = switcher.get(purpose, "Defpurp")
        if vr == "Defpurp":
            raise Exception("Not supported Purpose")
        return vr

    def __getStatus(self: GMEPublicOfferQuery, status: Status | None) -> str:
        if status is None:
            raise Exception("Not supported Status")

        switcher = {
            Status.ACC: "ACC",
            Status.INC: "INC",
            Status.REJ: "REJ",
            Status.REP: "REP",
            Status.REV: "REV",
            Status.SUB: "SUB",
            Status.COM: "COM",
            Status.PCOM: "PCOM",
        }
        vr = switcher.get(status, "DefStatus")
        if vr == "DefStatus":
            raise Exception("Not supported Status")
        return vr

    def __getUnitType(self: GMEPublicOfferQuery, unitType: UnitType) -> str:
        switcher = {
            UnitType.UP: "UP",
            UnitType.UC: "UC",
            UnitType.UPV: "UPV",
            UnitType.UCV: "UCV",
        }
        vr = switcher.get(unitType, "DefunitType")
        if vr == "DefunitType":
            raise Exception("Not supported Unit Type")
        return vr

    def __getBaType(self: GMEPublicOfferQuery, baType: BaType) -> str:
        switcher = {
            BaType.NULL: "NULL",
            BaType.NREV: "NREV",
            BaType.REV: "REV",
            BaType.NETT: "NETT",
        }
        vr = switcher.get(baType, "DefbaType")
        if vr == "DefbaType":
            raise Exception("Not supported BaType")
        return vr

    def __getZone(self: GMEPublicOfferQuery, zone: Zone) -> str:
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
            Zone.CALA: "CALA",
            Zone.MONT: "MONT",
        }
        vr = switcher.get(zone, "DefZone")
        if vr == "DefZone":
            raise Exception("Not supported Zone")
        return vr

    def _buildExtractionRangeRoute(
        self: GMEPublicOfferQuery, queryParamaters: _GMEPublicOfferQueryParameters
    ) -> str:
        subPath = f"{self.__toUrlParam(queryParamaters.extractionRangeConfig.date)}"
        return subPath

    def _exec(self: GMEPublicOfferQuery, url: str) -> Any:
        loop = get_event_loop()
        rr = loop.run_until_complete(self._execAsync(url))
        return rr

    async def _execAsync(self: GMEPublicOfferQuery, url: str) -> Any:
        with self.__client as c:
            res = await asyncio.gather(
                *[self.__executor.exec(c.exec, "GET", url, None)]
            )
            return res[0]

    def __toUrlParam(self: GMEPublicOfferQuery, date: str | None) -> str:
        return f"{date}"

    def _validateQuery(self: GMEPublicOfferQuery) -> None:
        if self._queryParameters.purpose is None:
            raise Exception(
                "Extraction Purpose must be provided. Use .forScope()"
                + " argument takes a scope type"
            )
        if self._queryParameters.extractionRangeConfig.date is None:
            raise Exception(
                "Extraction Date must be provided. Use .forDate() argument"
                + " takes a string formatted as YYYY-MM-DD"
            )
        if self._queryParameters.status is None:
            raise Exception(
                "Extraction Status must be provided. Use .forStatus() "
                + "argument takes a status type"
            )


def get_event_loop() -> asyncio.AbstractEventLoop:
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
