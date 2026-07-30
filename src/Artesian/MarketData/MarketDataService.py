from __future__ import annotations
from datetime import datetime
from typing import List, Optional, cast, Dict

from Artesian.MarketData._Dto import DeleteData
from Artesian.MarketData._Dto.DerivedTransformQueryValidation import DerivedTransformQueryValidation
from Artesian.MarketData._Dto.DerivedTransformQueryValidationResponse import DerivedTransformQueryValidationResponse
from ._Dto.DerivedCfg import DerivedCfg
from .._ClientsExecutor.RequestExecutor import _RequestExecutor
from .._ClientsExecutor.Client import _Client
from ..ArtesianConfig import ArtesianConfig
from ..ArtesianPolicyConfig import ArtesianPolicyConfig
from ._Dto.PagedResult import (
    PagedResultCurveRangeEntity,
    PagedResultDataQualityRuleDtoOutput,
    PagedResultMarketDataQualityRuleAssignmentDtoOutput,
)
from ._Dto.ArtesianSearchResults import ArtesianSearchResults
from ._Dto.MarketDataEntityInput import MarketDataEntityInput
from ._Dto.MarketDataEntityOutput import MarketDataEntityOutput
from ._Dto.CheckConversionResult import CheckConversionResult
from ._Dto.UpsertData import UpsertData
from ._Dto.DataQualityRuleDtoInput import DataQualityRuleDtoInput
from ._Dto.DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from ._Dto.DqCheckChangeEventDto import DqCheckChangeEventDtoOutput
from ._Dto.MarketDataQualityRuleAssignmentDto import (
    MarketDataQualityRuleAssignmentDtoInput,
    MarketDataQualityRuleAssignmentDtoOutput,
)
from ._Enum.RuleType import RuleType
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

    async def registerDataQualityRuleAsync(
        self: MarketDataService, entity: DataQualityRuleDtoInput
    ) -> DataQualityRuleDtoOutput:
        """
        Creates a new Data Quality Rule.

        Args:
            entity: rule definition including name, type and configuration.

        Returns:
            Created DataQualityRuleDtoOutput (Async).
        """
        url = "/dataquality/dqrule"
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "POST", url, entity, DataQualityRuleDtoOutput
                    )
                ]
            )
            return cast(DataQualityRuleDtoOutput, res[0])

    def registerDataQualityRule(
        self: MarketDataService, entity: DataQualityRuleDtoInput
    ) -> DataQualityRuleDtoOutput:
        """
        Creates a new Data Quality Rule.

        Args:
            entity: rule definition including name, type and configuration.

        Returns:
            Created DataQualityRuleDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.registerDataQualityRuleAsync(entity)
        )

    async def readDataQualityRuleByIdAsync(
        self: MarketDataService, id: int
    ) -> DataQualityRuleDtoOutput:
        """
        Retrieves a Data Quality Rule by its id.

        Args:
            id: unique identifier of the rule.

        Returns:
            DataQualityRuleDtoOutput (Async).
        """
        url = "/dataquality/dqrule/" + str(id)
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "GET", url, None, retcls=DataQualityRuleDtoOutput
                    )
                ]
            )
            return cast(DataQualityRuleDtoOutput, res[0])

    def readDataQualityRuleById(
        self: MarketDataService, id: int
    ) -> DataQualityRuleDtoOutput:
        """
        Retrieves a Data Quality Rule by its id.

        Args:
            id: unique identifier of the rule.

        Returns:
            DataQualityRuleDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.readDataQualityRuleByIdAsync(id)
        )

    async def readDataQualityRuleAsync(
        self: MarketDataService,
        page: int,
        pageSize: int,
        type: Optional[RuleType] = None,
        marketDataId: Optional[int] = None,
        name: Optional[str] = None,
        ruleIds: Optional[List[int]] = None,
        sort: Optional[List[str]] = None,
    ) -> PagedResultDataQualityRuleDtoOutput:
        """
        Retrieves a paginated list of Data Quality Rules.

        Args:
            page: page number (1-based).
            pageSize: number of items per page.
            type: optional filter by rule type.
            marketDataId: optional filter for assigned MarketData id.
            name: optional partial filter by rule name.
            ruleIds: optional filter by specific rule ids.
            sort: optional sort expressions.

        Returns:
            PagedResultDataQualityRuleDtoOutput (Async).
        """
        if page < 1:
            raise ValueError(f"page must be >= 1 (got {page})")
        if pageSize < 1:
            raise ValueError(f"pageSize must be >= 1 (got {pageSize})")

        params = {}
        params["page"] = page
        params["pageSize"] = pageSize
        if type is not None:
            params["type"] = type.name
        if marketDataId is not None:
            params["marketDataId"] = marketDataId
        if name:
            params["name"] = name
        if ruleIds:
            params["ruleIds"] = ruleIds
        if sort:
            params["sort"] = sort

        url = "/dataquality/dqrule"
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=PagedResultDataQualityRuleDtoOutput,
                        params=params,
                    )
                ]
            )
            return cast(PagedResultDataQualityRuleDtoOutput, res[0])

    def readDataQualityRule(
        self: MarketDataService,
        page: int,
        pageSize: int,
        type: Optional[RuleType] = None,
        marketDataId: Optional[int] = None,
        name: Optional[str] = None,
        ruleIds: Optional[List[int]] = None,
        sort: Optional[List[str]] = None,
    ) -> PagedResultDataQualityRuleDtoOutput:
        """
        Retrieves a paginated list of Data Quality Rules.

        Args:
            page: page number (1-based).
            pageSize: number of items per page.
            type: optional filter by rule type.
            marketDataId: optional filter for assigned MarketData id.
            name: optional partial filter by rule name.
            ruleIds: optional filter by specific rule ids.
            sort: optional sort expressions.

        Returns:
            PagedResultDataQualityRuleDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.readDataQualityRuleAsync(
                page,
                pageSize,
                type,
                marketDataId,
                name,
                ruleIds,
                sort,
            )
        )

    async def updateDataQualityRuleAsync(
        self: MarketDataService, id: int, entity: DataQualityRuleDtoInput
    ) -> DataQualityRuleDtoOutput:
        """
        Updates an existing Data Quality Rule.

        Args:
            id: unique identifier of the rule to update.
            entity: updated rule definition.

        Returns:
            Updated DataQualityRuleDtoOutput (Async).
        """
        url = "/dataquality/dqrule/" + str(id)
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec, "PUT", url, entity, DataQualityRuleDtoOutput
                    )
                ]
            )
            return cast(DataQualityRuleDtoOutput, res[0])

    def updateDataQualityRule(
        self: MarketDataService, id: int, entity: DataQualityRuleDtoInput
    ) -> DataQualityRuleDtoOutput:
        """
        Updates an existing Data Quality Rule.

        Args:
            id: unique identifier of the rule to update.
            entity: updated rule definition.

        Returns:
            Updated DataQualityRuleDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.updateDataQualityRuleAsync(id, entity)
        )

    async def deleteDataQualityRuleAsync(self: MarketDataService, id: int) -> None:
        """
        Deletes a Data Quality Rule by id.

        Args:
            id: unique identifier of the rule to delete.

        Returns:
            None (Async).
        """
        url = "/dataquality/dqrule/" + str(id)
        with self.__client as c:
            await asyncio.gather(*[self.__executor.exec(c.exec, "DELETE", url, None)])
            return None

    def deleteDataQualityRule(self: MarketDataService, id: int) -> None:
        """
        Deletes a Data Quality Rule by id.

        Args:
            id: unique identifier of the rule to delete.

        Returns:
            None.
        """
        return _get_event_loop().run_until_complete(
            self.deleteDataQualityRuleAsync(id)
        )

    async def registerDataQualityRuleAssignmentAsync(
        self: MarketDataService,
        entity: MarketDataQualityRuleAssignmentDtoInput,
        initializationLookbackPeriod: Optional[str] = None,
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Creates a new assignment binding a Market Data entity to a Data Quality Rule.

        Args:
            entity: assignment definition including MarketDataId and DataQualityRuleId.
            initializationLookbackPeriod: optional ISO 8601 period (e.g. "P30D")
                defining how far back in time the rule should validate data on
                initial assignment.

        Returns:
            Created MarketDataQualityRuleAssignmentDtoOutput (Async).
        """
        if entity is None:
            raise ValueError("entity cannot be None")

        url = "/dataquality/dqruleassignment"
        params = {}
        if initializationLookbackPeriod is not None:
            params["initializationLookbackPeriod"] = initializationLookbackPeriod

        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "POST",
                        url,
                        entity,
                        retcls=MarketDataQualityRuleAssignmentDtoOutput,
                        params=params,
                    )
                ]
            )
            return cast(MarketDataQualityRuleAssignmentDtoOutput, res[0])

    def registerDataQualityRuleAssignment(
        self: MarketDataService,
        entity: MarketDataQualityRuleAssignmentDtoInput,
        initializationLookbackPeriod: Optional[str] = None,
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Creates a new assignment binding a Market Data entity to a Data Quality Rule.

        Args:
            entity: assignment definition including MarketDataId and DataQualityRuleId.
            initializationLookbackPeriod: optional ISO 8601 period (e.g. "P30D")
                defining how far back in time the rule should validate data on
                initial assignment.

        Returns:
            Created MarketDataQualityRuleAssignmentDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.registerDataQualityRuleAssignmentAsync(
                entity,
                initializationLookbackPeriod,
            )
        )

    async def readDataQualityRuleAssignmentByIdAsync(
        self: MarketDataService, id: int
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Retrieves a DQ rule assignment by its unique identifier.

        Args:
            id: unique identifier of the assignment.

        Returns:
            MarketDataQualityRuleAssignmentDtoOutput (Async).
        """
        url = "/dataquality/dqruleassignment/" + str(id)

        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=MarketDataQualityRuleAssignmentDtoOutput,
                    )
                ]
            )
            return cast(MarketDataQualityRuleAssignmentDtoOutput, res[0])

    def readDataQualityRuleAssignmentById(
        self: MarketDataService, id: int
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Retrieves a DQ rule assignment by its unique identifier.

        Args:
            id: unique identifier of the assignment.

        Returns:
            MarketDataQualityRuleAssignmentDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.readDataQualityRuleAssignmentByIdAsync(id)
        )

    async def readDataQualityRuleAssignmentAsync(
        self: MarketDataService,
        page: int,
        pageSize: int,
        marketDataId: Optional[int] = None,
        ruleId: Optional[int] = None,
        ruleName: Optional[str] = None,
        sort: Optional[List[str]] = None,
    ) -> PagedResultMarketDataQualityRuleAssignmentDtoOutput:
        """
        Retrieves a paginated list of DQ rule assignments.

        Args:
            page: page number (1-based).
            pageSize: number of items per page.
            marketDataId: optional filter by Market Data id.
            ruleId: optional filter by Data Quality Rule id.
            ruleName: optional partial filter by rule name.
            sort: optional sort expressions.

        Returns:
            PagedResultMarketDataQualityRuleAssignmentDtoOutput (Async).
        """
        if page < 1:
            raise ValueError("Page must to be greater than 0. Page:" + str(page))
        if pageSize < 1:
            raise ValueError(
                "PageSize must to be greater than 0. Page Size:" + str(pageSize)
            )

        params = {}
        params["page"] = page
        params["pageSize"] = pageSize
        if marketDataId is not None:
            params["marketDataId"] = marketDataId
        if ruleId is not None:
            params["ruleId"] = ruleId
        if ruleName:
            params["ruleName"] = ruleName
        if sort:
            params["sort"] = sort

        url = "/dataquality/dqruleassignment"
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=PagedResultMarketDataQualityRuleAssignmentDtoOutput,
                        params=params,
                    )
                ]
            )
            return cast(PagedResultMarketDataQualityRuleAssignmentDtoOutput, res[0])

    def readDataQualityRuleAssignment(
        self: MarketDataService,
        page: int,
        pageSize: int,
        marketDataId: Optional[int] = None,
        ruleId: Optional[int] = None,
        ruleName: Optional[str] = None,
        sort: Optional[List[str]] = None,
    ) -> PagedResultMarketDataQualityRuleAssignmentDtoOutput:
        """
        Retrieves a paginated list of DQ rule assignments.

        Args:
            page: page number (1-based).
            pageSize: number of items per page.
            marketDataId: optional filter by Market Data id.
            ruleId: optional filter by Data Quality Rule id.
            ruleName: optional partial filter by rule name.
            sort: optional sort expressions.

        Returns:
            PagedResultMarketDataQualityRuleAssignmentDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.readDataQualityRuleAssignmentAsync(
                page,
                pageSize,
                marketDataId,
                ruleId,
                ruleName,
                sort,
            )
        )

    async def updateDataQualityRuleAssignmentAsync(
        self: MarketDataService,
        id: int,
        initializationLookbackPeriod: str,
        etag: str,
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Updates an assignment lookback, triggering re-evaluation from new date.

        Args:
            id: unique identifier of the assignment to update.
            initializationLookbackPeriod: ISO 8601 period (e.g. "P30D").
            etag: current ETag for optimistic concurrency control.

        Returns:
            Updated MarketDataQualityRuleAssignmentDtoOutput (Async).
        """
        url = "/dataquality/dqruleassignment/" + str(id)
        params = {
            "initializationLookbackPeriod": initializationLookbackPeriod,
            "etag": etag,
        }

        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "PUT",
                        url,
                        None,
                        retcls=MarketDataQualityRuleAssignmentDtoOutput,
                        params=params,
                    )
                ]
            )
            return cast(MarketDataQualityRuleAssignmentDtoOutput, res[0])

    def updateDataQualityRuleAssignment(
        self: MarketDataService,
        id: int,
        initializationLookbackPeriod: str,
        etag: str,
    ) -> MarketDataQualityRuleAssignmentDtoOutput:
        """
        Updates an assignment lookback, triggering re-evaluation from new date.

        Args:
            id: unique identifier of the assignment to update.
            initializationLookbackPeriod: ISO 8601 period (e.g. "P30D").
            etag: current ETag for optimistic concurrency control.

        Returns:
            Updated MarketDataQualityRuleAssignmentDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.updateDataQualityRuleAssignmentAsync(
                id,
                initializationLookbackPeriod,
                etag,
            )
        )

    async def deleteDataQualityRuleAssignmentAsync(
        self: MarketDataService, id: int
    ) -> None:
        """
        Deletes an assignment by id.

        Args:
            id: unique identifier of the assignment to delete.

        Returns:
            None (Async).
        """
        url = "/dataquality/dqruleassignment/" + str(id)
        with self.__client as c:
            await asyncio.gather(*[self.__executor.exec(c.exec, "DELETE", url, None)])
            return None

    def deleteDataQualityRuleAssignment(self: MarketDataService, id: int) -> None:
        """
        Deletes an assignment by id.

        Args:
            id: unique identifier of the assignment to delete.

        Returns:
            None.
        """
        return _get_event_loop().run_until_complete(
            self.deleteDataQualityRuleAssignmentAsync(id)
        )

    async def readDataQualityRuleAssignmentEventsFeedAsync(
        self: MarketDataService,
        id: int,
        afterTimestamp: Optional[datetime] = None,
    ) -> List[DqCheckChangeEventDtoOutput]:
        """
        Retrieves the raw event feed for a specific rule assignment.

        Args:
            id: rule assignment identifier.
            afterTimestamp: optional lower bound, returns events after instant.

        Returns:
            List of DqCheckChangeEventDtoOutput (Async).
        """
        url = "/dataquality/dqruleassignment/" + str(id) + "/events"
        params = {}
        if afterTimestamp is not None:
            params["afterTimestamp"] = afterTimestamp.isoformat()
        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "GET",
                        url,
                        None,
                        retcls=List[DqCheckChangeEventDtoOutput],
                        params=params,
                    )
                ]
            )
            return cast(List[DqCheckChangeEventDtoOutput], res[0])

    def readDataQualityRuleAssignmentEventsFeed(
        self: MarketDataService,
        id: int,
        afterTimestamp: Optional[datetime] = None,
    ) -> List[DqCheckChangeEventDtoOutput]:
        """
        Retrieves the raw event feed for a specific rule assignment.

        Args:
            id: rule assignment identifier.
            afterTimestamp: optional lower bound, returns events after instant.

        Returns:
            List of DqCheckChangeEventDtoOutput.
        """
        return _get_event_loop().run_until_complete(
            self.readDataQualityRuleAssignmentEventsFeedAsync(id, afterTimestamp)
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

    async def derivedTransformQueryValidationAsync(
        self: MarketDataService,
        request: DerivedTransformQueryValidation
    ) -> DerivedTransformQueryValidationResponse:
        """
        Derived Transform Query Validation.

        Args:
            request: Request containing TimeSerieData and the Query to be applied to verify the derived transformation
        Returns:
            DerivedTransformQueryValidationResponse Entity (Async).
        """
        url = "/utils/derivedTransform/queryValidation"

        with self.__client as c:
            res = await asyncio.gather(
                *[
                    self.__executor.exec(
                        c.exec,
                        "POST",
                        url,
                        request,
                        retcls=DerivedTransformQueryValidationResponse
                    )
                ]
            )

            return cast(DerivedTransformQueryValidationResponse, res[0])

    def derivedTransformQueryValidation(
        self: MarketDataService,
        request: DerivedTransformQueryValidation
    ) -> DerivedTransformQueryValidationResponse:
        """
        Derived Transform Query Validation.

        Args:
            request: Request containing TimeSerieData and the Query to be applied to verify the derived transformation

        Returns:
            DerivedTransformQueryValidationResponse Entity.
        """

        return _get_event_loop().run_until_complete(
            self.derivedTransformQueryValidationAsync(request)
        )


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
