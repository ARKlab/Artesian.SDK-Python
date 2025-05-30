from __future__ import annotations
from typing import List, Optional, cast, Dict

from Artesian.MarketData._Dto import DeleteData
from ._Dto.DerivedCfg import DerivedCfg
from .._ClientsExecutor.RequestExecutor import _RequestExecutor
from .._ClientsExecutor.Client import _Client
from ..ArtesianConfig import ArtesianConfig
from ..ArtesianPolicyConfig import ArtesianPolicyConfig
from ._Dto.PagedResult import PagedResultCurveRangeEntity
from ._Dto.ArtesianSearchResults import ArtesianSearchResults
from ._Dto.MarketDataEntityInput import MarketDataEntityInput
from ._Dto.MarketDataEntityOutput import MarketDataEntityOutput
from ._Dto.CheckConversionResult import CheckConversionResult
from ._Dto.UpsertData import UpsertData
import asyncio


class MarketDataService:
    """
    Class for the MarketData Service.

    """

    __version = "v2.1"

    def __init__(self: MarketDataService, artesianConfig: ArtesianConfig) -> None:
        """
        Inits the MarketData Service

        Using the ArtesianServiceConfig, is possible to create an istance of
        the MarketDataService which is used to retrieve and edit MarketData references.

        Args:
            artesianConfiguration: The Artesian Configuration.

        """
        self.__config = artesianConfig
        self.__policy = ArtesianPolicyConfig()
        self.__serviceBaseurl = self.__config.baseUrl + "/" + self.__version
        self.__executor = _RequestExecutor(self.__policy)
        self.__client = _Client(self.__serviceBaseurl, self.__config.apiKey)

    async def readCurveRangeAsync(
        self: MarketDataService,
        id: int,
        page: int,
        pageSize: int,
        product: Optional[str] = None,
        versionFrom: Optional[str] = None,
        versionTo: Optional[str] = None,
    ) -> PagedResultCurveRangeEntity:
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
        params = {}  # needed to avoid typing to detect dict[str,int] ...
        params["page"] = page
        params["pageSize"] = pageSize
        if versionFrom is not None:
            params["versionFrom"] = versionFrom
        if versionTo is not None:
            params["versionTo"] = versionTo
        if product is not None:
            params["product"] = product
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        retcls=PagedResultCurveRangeEntity,
                        params=params,
                    )
                ]
            )
            return cast(PagedResultCurveRangeEntity, res[0])

    def readCurveRange(
        self: MarketDataService,
        id: int,
        page: int,
        pageSize: int,
        product: Optional[str] = None,
        versionFrom: Optional[str] = None,
        versionTo: Optional[str] = None,
    ) -> PagedResultCurveRangeEntity:
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
        return _get_event_loop().run_until_complete(
            self.readCurveRangeAsync(
                id, page, pageSize, product, versionFrom, versionTo
            )
        )

    async def searchFacetAsync(
        self: MarketDataService,
        page: int,
        pageSize: int,
        searchText: str | None = None,
        filters: Optional[Dict[str, List[str]]] = None,
        sorts: Optional[List[str]] = None,
        doNotLoadAdditionalInfo: bool = False,
    ) -> ArtesianSearchResults:
        """
        Search the MarketData collection with faceted results.

        Args:
            searchText: SearchText parameter.
            page: int of the page number (1-based).
            pageSize: int of the pagesize.
            filters: ArtesianSearchFilter containing the search params.
            sorts: Sorts list.
            doNotLoadAdditionalInfo: Skip loading up-to-date curve range and transform.

        Returns:
            ArtesianSearchResults entity (Async).
        """
        filtersList = None

        if filters is not None:
            filtersList = []
            for key, values in filters.items():
                for value in values:
                    filtersList.append(key + ":" + value)

        url = "/marketdata/searchfacet"
        params = {}  # needed to avoid typing to detect dict[str,int] ...
        params["page"] = page
        params["pageSize"] = pageSize
        params["searchText"] = searchText
        if filters is not None:
            params["filters"] = filtersList
        if sorts is not None:
            params["sorts"] = sorts
        params["doNotLoadAdditionalInfo"] = doNotLoadAdditionalInfo

        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        retcls=ArtesianSearchResults,
                        params=params,
                    )
                ]
            )
            return cast(ArtesianSearchResults, res[0])

    def searchFacet(
        self: MarketDataService,
        page: int,
        pageSize: int,
        searchText: Optional[str] = None,
        filters: Optional[Dict[str, List[str]]] = None,
        sorts: Optional[List[str]] = None,
        doNotLoadAdditionalInfo: bool = False,
    ) -> ArtesianSearchResults:
        """
        Search the MarketData collection with faceted results.

        Args:
            searchText: SearchText parameter.
            page: int of the page number (1-based).
            pageSize: int of the pagesize.
            filters: ArtesianSearchFilter containing the search params.
            sorts: Sorts list.
            doNotLoadAdditionalInfo: Skip loading up-to-date curve range and transform.

        Returns:
            ArtesianSearchResults entity.
        """
        return _get_event_loop().run_until_complete(
            self.searchFacetAsync(
                page, pageSize, searchText, filters, sorts, doNotLoadAdditionalInfo
            )
        )

    async def readMarketDataRegistryByIdAsync(
        self: MarketDataService, id: int
    ) -> MarketDataEntityOutput:
        """
        Reads MarketData by id with MarketDataID.

        Args:
            id: ID of the marketdata to be retrieved.

        Returns:
            MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id)
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "GET", url, None, retcls=MarketDataEntityOutput
                    )
                ]
            )
            return cast(MarketDataEntityOutput, res[0])

    def readMarketDataRegistryById(
        self: MarketDataService, id: int
    ) -> MarketDataEntityOutput:
        """
        Reads MarketData by curve name with MarketDataID.

        Args:
            id: ID of the marketdata to be retrieved.

        Returns:
            MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(
            self.readMarketDataRegistryByIdAsync(id)
        )

    async def updateMarketDataAsync(
        self: MarketDataService, id: int, entity: MarketDataEntityInput
    ) -> MarketDataEntityOutput:
        """
        Saves the given MarketData Entity

        Args:
            id: int of the marketdata to be updated

        Returns:
            MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id)
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "PUT", url, entity, MarketDataEntityOutput
                    )
                ]
            )
            return cast(MarketDataEntityOutput, res[0])

    def updateMarketData(
        self: MarketDataService, id: int, entity: MarketDataEntityInput
    ) -> MarketDataEntityOutput:
        """
        Saves the given MarketData Entity

        Args:
            id: int of the marketdata to be updated

        Returns:
            MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(
            self.updateMarketDataAsync(id, entity)
        )

    async def deleteMarketDataAsync(self: MarketDataService, id: int) -> None:
        """
        Delete the specific MarketData entity by id

        Args:
            id: int of the marketdata to be deleted

        Returns:
            MarketData Entity Output (Async).
        """
        url = "/marketdata/entity/" + str(id)
        with self.__client as c:
            await asyncio.gather(*[self.__executor.exec(c.exec, "DELETE", url, None)])
            return None

    def deleteMarketData(self: MarketDataService, id: int) -> None:
        """
        Delete the specific MarketData entity by id

        Args:
            id: int of the marketdata to be deleted

        Returns:
            MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(self.deleteMarketDataAsync(id))

    async def readMarketDataRegistryByNameAsync(
        self: MarketDataService, provider: str, curveName: str
    ) -> MarketDataEntityOutput:
        """
        Reads MarketData by provider and curve name.

        Args:
            provider: string of the provider to be retrieved.
            curveName: string of the curve name to be retrieved.

        Returns:
            MarketData Entity Output (Async).
        """
        url = "/marketdata/entity"
        params = {"provider": provider, "curveName": curveName}
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=MarketDataEntityOutput,
                        params=params,
                    )
                ]
            )
            return cast(MarketDataEntityOutput, res[0])

    def readMarketDataRegistryByName(
        self: MarketDataService, provider: str, curveName: str
    ) -> MarketDataEntityOutput:
        """
        Reads MarketData by provider and curve name.

        Args:
            provider: string of the provider to be retrieved.
            curveName: string of the curve name to be retrieved.

        Returns:
            MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(
            self.readMarketDataRegistryByNameAsync(provider, curveName)
        )

    async def registerMarketDataAsync(
        self: MarketDataService, entity: MarketDataEntityInput
    ) -> MarketDataEntityOutput:
        """
        Register a new MarketData entity.

        Args:
            entity: The Market Data Entity Input

        Returns:
            MarketData Entity Output (Async).
        """
        url = "/marketdata/entity"
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "POST", url, entity, MarketDataEntityOutput
                    )
                ]
            )
            return cast(MarketDataEntityOutput, res[0])

    def registerMarketData(
        self: MarketDataService, entity: MarketDataEntityInput
    ) -> MarketDataEntityOutput:
        """
        Register a new MarketData entity.

        Args:
            entity: The Market Data Entity Input

        Returns:
            MarketData Entity Output.
        """

        entity._validateDerivedCfg()

        return _get_event_loop().run_until_complete(
            self.registerMarketDataAsync(entity)
        )

    async def checkConversionAsync(
        self: MarketDataService,
        inputUnitsOfMeasure: List[str],
        targetUnitOfMeasure: str
    ) -> CheckConversionResult:
        """
        Check UnitOfMeasure conversion.

        Args:
            inputUnitsOfMeasure: the list of the input UnitOfMeasure to be check for
                                conversion
            targetUnitOfMeasure: The target UnitOfMeasure

        Returns:
            CheckConversionResult Entity (Async).
        """
        url = "/uom/checkconversion"
        params = {"inputUnitsOfMeasure": inputUnitsOfMeasure,
                  "targetUnitOfMeasure": targetUnitOfMeasure}
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=CheckConversionResult,
                        params=params,
                    )
                ]
            )
            return cast(CheckConversionResult, res[0])

    def checkConversion(
        self: MarketDataService,
        inputUnitsOfMeasure: List[str],
        targetUnitOfMeasure: str
    ) -> CheckConversionResult:
        """
        Check UnitOfMeasure conversion.

        Args:
            inputUnitsOfMeasure: the list of the input UnitOfMeasure to be check for
                                conversion
            targetUnitOfMeasure: The target UnitOfMeasure

        Returns:
            CheckConversionResult Entity.
        """

        return _get_event_loop().run_until_complete(
            self.checkConversionAsync(inputUnitsOfMeasure, targetUnitOfMeasure)
        )

    async def updateDerivedConfigurationAsync(
        self: MarketDataService,
        marketDataId: int,
        derivedCfg: DerivedCfg,
        force: bool = False
    ) -> MarketDataEntityOutput:
        """
        Update Derived Configuration for marketData with id supplied in MarketDataId.
        The update will trigger a Rebuild

        Args:
            marketDataId: The Market Data Id to be updated
            derivedCfg: The Derived Configuration to be updated
            force: Force the update of configuration also if another
                   rebuild process is running (Default=false)

        Returns:
            MarketData Entity Output (Async).
        """

        marketDataOutput = await self.readMarketDataRegistryByIdAsync(marketDataId)

        marketDataOutput._validateUpdateDerivedCfg(derivedCfgUpdate=derivedCfg)

        url = "/marketdata/entity/" + str(marketDataId) + "/updateDerivedConfiguration"
        params = {"force": force}
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "POST",
                        url,
                        derivedCfg,
                        retcls=MarketDataEntityOutput,
                        params=params,
                    )
                ]
            )
            return cast(MarketDataEntityOutput, res[0])

    def updateDerivedConfiguration(
        self: MarketDataService,
        marketDataId: int,
        derivedCfg: DerivedCfg,
        force: bool = False
    ) -> MarketDataEntityOutput:
        """
        Update Derived Configuration for marketData with id supplied in MarketDataId.
        The update will trigger a Rebuild

        Args:
            marketDataId: The Market Data Id to be updated
            derivedCfg: The Derived Configuration to be updated
            force: Force the update of configuration also if another
                   rebuild process is running (Default=false)

        Returns:
            MarketData Entity Output.
        """
        return _get_event_loop().run_until_complete(
            self.updateDerivedConfigurationAsync(marketDataId, derivedCfg, force)
        )

    async def upsertDataAsync(self: MarketDataService, data: UpsertData) -> None:
        url = "/marketdata/upsertdata"
        with self.__client as c:
            await asyncio.gather(*[self.__executor.exec(c.exec, "POST", url, data)])
            return None

    def upsertData(self: MarketDataService, data: UpsertData) -> None:
        return _get_event_loop().run_until_complete(self.upsertDataAsync(data))

    async def deleteDataAsync(self: MarketDataService, data: DeleteData) -> None:
        url = "/marketdata/deletedata"
        with self.__client as c:
            await asyncio.gather(*[self.__executor.exec(c.exec, "POST", url, data)])
            return None

    def deleteData(self: MarketDataService, data: DeleteData) -> None:
        return _get_event_loop().run_until_complete(self.deleteDataAsync(data))


def _get_event_loop() -> asyncio.AbstractEventLoop:
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
