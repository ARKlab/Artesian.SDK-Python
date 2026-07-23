from Artesian import ArtesianConfig
import responses
import unittest
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from Artesian.MarketData import *
from Artesian.MarketData._Dto.ActualCompletenessAndFreshnessConfigDto import (
    ActualCompletenessAndFreshnessConfigDto,
)
from Artesian.MarketData._Dto.CronScheduleDefinitionDto import CronScheduleDefinitionDto
from Artesian.MarketData._Dto.DataQualityRuleConfigDto import DataQualityRuleConfigDto
from Artesian.MarketData._Dto.DataQualityRuleDtoInput import DataQualityRuleDtoInput
from Artesian.MarketData._Dto.DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from Artesian.MarketData._Dto.MarketDataQualityRuleAssignmentDto import (
    MarketDataQualityRuleAssignmentDtoInput,
    MarketDataQualityRuleAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.PagedResult import (
    PagedResultDataQualityRuleDtoOutput,
    PagedResultMarketDataQualityRuleAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.RecordValidationConfigDto import RecordValidationConfigDto
from Artesian.MarketData._Dto.ScheduleConfigDto import ScheduleConfigDto
from Artesian.MarketData._Enum.MarketDataTypeV2 import MarketDataTypeV2
from Artesian.MarketData._Enum.RuleType import RuleType

cfg = ArtesianConfig("https://baseurl.com", "APIKey")


class TestMarketDataServiceMarketData(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__service = MarketDataService(cfg)
        
        curveIds = [1, 2]
        derivedCfg = DerivedCfg(
                        version=1,
                        derivedAlgorithm=DerivedAlgorithm.Coalesce,
                        orderedReferencedMarketDataIds=curveIds,
                    )
        
        self.__sampleOutput = MarketDataEntityOutput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataType.ActualTimeSerie,
            originalTimezone="CET",
            tags={"PythonTag": ["PythonTagValue1", "PythonTagValue2"]},
            derivedCfg=derivedCfg,
            unitOfMeasure=UnitOfMeasure(value=CommonUnitOfMeasure.MW)
        )
        self.__serializedOutput = artesianJsonSerialize(self.__sampleOutput)
        self.__sampleInput = MarketDataEntityInput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataType.ActualTimeSerie,
            originalTimezone="CET",
            tags={"PythonTag": ["PythonTagValue1", "PythonTagValue2"]},
            derivedCfg=derivedCfg,
            unitOfMeasure=UnitOfMeasure(value=CommonUnitOfMeasure.MW)
        )
        self.maxDiff = None
        self.__baseurl = "https://baseurl.com/v2.1"
        self.__id = 1
        self.__curveRangeOutput = PagedResultCurveRangeEntity(
            1, 2, 1, False, [CurveRangeEntity(self.__id)]
        )
        self.__curveRangeSerializedOutput = artesianJsonSerialize(
            self.__curveRangeOutput
        )
        self.__artesianMetadataFacetCount = ArtesianMetadataFacetCount(
            value="TestValue", count=1
        )
        self.__artesianMetadataFacet = ArtesianMetadataFacet(
            facetName="TestFacet",
            facetType=ArtesianMetadataFacetType.Tag,
            values=[self.__artesianMetadataFacetCount],
        )
        self.__artesianSearchResults = ArtesianSearchResults(
            results=[self.__sampleOutput],
            facets=[self.__artesianMetadataFacet],
            countResults=1,
        )
        self.__artesianSearchResultsSerializedOutput = artesianJsonSerialize(
            self.__artesianSearchResults
        )
        self.__checkConversionResult = CheckConversionResult(
            targetUnitOfMeasure=CommonUnitOfMeasure.kW,
            convertibleInputUnitsOfMeasure=[ CommonUnitOfMeasure.MW, CommonUnitOfMeasure.MWh ],
            notConvertibleInputUnitsOfMeasure=[ CommonUnitOfMeasure.day ]
        )
        self.__checkConversionResultSerializedOutput = artesianJsonSerialize(
            self.__checkConversionResult
        )
        self.__dataQualityRuleConfig = ActualCompletenessAndFreshnessConfigDto(
            marketDataType=MarketDataTypeV2.ActualTimeSerie,
            scheduleConfig=ScheduleConfigDto(
                scheduleDefinition=CronScheduleDefinitionDto(
                    cronExpression="0 0 * * *",
                    timeZone="UTC",
                ),
                maxDelay="PT1H",
            ),
            recordValidationConfig=RecordValidationConfigDto(
                recordRangeFrom="PT0S",
                recordRangeTo="PT1H",
            ),
        )
        self.__dataQualityRuleInput = DataQualityRuleDtoInput(
            id=0,
            name="TestRule",
            type=RuleType.CompletenessAndFreshness,
            configuration=self.__dataQualityRuleConfig,
            version=0,
        )
        self.__dataQualityRuleInputSerialized = artesianJsonSerialize(
            self.__dataQualityRuleInput
        )
        self.__dataQualityRuleOutput = DataQualityRuleDtoOutput(
            id=1,
            name="TestRule",
            type=RuleType.CompletenessAndFreshness,
            configuration=DataQualityRuleConfigDto(
                type=RuleType.CompletenessAndFreshness
            ),
            version=1,
            eTag="etag-1",
        )
        self.__dataQualityRuleOutputSerialized = artesianJsonSerialize(
            self.__dataQualityRuleOutput
        )
        self.__pagedDataQualityRuleOutput = PagedResultDataQualityRuleDtoOutput(
            1,
            10,
            1,
            False,
            [self.__dataQualityRuleOutput],
        )
        self.__pagedDataQualityRuleOutputSerialized = artesianJsonSerialize(
            self.__pagedDataQualityRuleOutput
        )
        self.__dataQualityRuleAssignmentInput = MarketDataQualityRuleAssignmentDtoInput(
            marketDataId=100,
            dataQualityRuleId=1,
        )
        self.__dataQualityRuleAssignmentInputSerialized = artesianJsonSerialize(
            self.__dataQualityRuleAssignmentInput
        )
        self.__dataQualityRuleAssignmentOutput = (
            MarketDataQualityRuleAssignmentDtoOutput(
                id=1,
                marketDataId=100,
                dataQualityRuleId=1,
                eTag="test-etag",
                version=1,
            )
        )
        self.__dataQualityRuleAssignmentOutputSerialized = artesianJsonSerialize(
            self.__dataQualityRuleAssignmentOutput
        )
        self.__pagedDataQualityRuleAssignmentOutput = (
            PagedResultMarketDataQualityRuleAssignmentDtoOutput(
                1,
                10,
                1,
                False,
                [self.__dataQualityRuleAssignmentOutput],
            )
        )
        self.__pagedDataQualityRuleAssignmentOutputSerialized = artesianJsonSerialize(
            self.__pagedDataQualityRuleAssignmentOutput
        )

        return super().setUp()

    async def test_registerMarketData(self):
        expectedJson = {
            "MarketDataId": 0,
            "ProviderName": "PROVIDER",
            "MarketDataName": "MARKETDATA",
            "OriginalGranularity": "Day",
            "Type": "ActualTimeSerie",
            "OriginalTimezone": "CET",
            "UnitOfMeasure":
            {
                "Value": "MW"
            },
            "Tags": [
                {"Key": "PythonTag", "Value": ["PythonTagValue1", "PythonTagValue2"]}
            ],
            "AggregationRule": "Undefined",
            "DerivedCfg":
            {
                "DerivedAlgorithm": "Coalesce",
                "Version": 1,
                "OrderedReferencedMarketDataIds": [1, 2]
            }
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/entity",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                json=self.__serializedOutput,
                status=200,
            )

            output = await self.__service.registerMarketDataAsync(self.__sampleInput)

            self.assertEqual(output, self.__sampleOutput)

    async def test_readMarketDataRegistryByNameAsync(self):
        with responses.RequestsMock() as rsps:
            params = {"provider": "PROVIDER", "curveName": "MARKETDATA"}
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__serializedOutput,
                status=200,
            )
            output = await self.__service.readMarketDataRegistryByNameAsync(
                params["provider"], params["curveName"]
            )
            self.assertEqual(output, self.__sampleOutput)

    async def test_deleteMarketDataAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/marketdata/entity/" + str(self.__id),
                status=204,
            )
            await self.__service.deleteMarketDataAsync(self.__id)
            self.assertEqual(len(rsps.calls), 1)

    async def test_updateMarketDataAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "PUT",
                self.__baseurl + "/marketdata/entity/" + str(self.__id),
                json=self.__serializedOutput,
                status=200,
            )
            output = await self.__service.updateMarketDataAsync(
                self.__id, self.__sampleInput
            )
            self.assertEqual(output, self.__sampleOutput)

    async def test_readMarketDataRegistryByIdAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity/" + str(self.__id),
                json=self.__serializedOutput,
                status=200,
            )
            output = await self.__service.readMarketDataRegistryByIdAsync(self.__id)
            self.assertEqual(output, self.__sampleOutput)

    async def test_readCurveRangePaginationAsync(self):
        with responses.RequestsMock() as rsps:
            params = {"page": "1", "pageSize": "2"}
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity/" + str(self.__id) + "/curves",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__curveRangeSerializedOutput,
                status=200,
            )
            output = await self.__service.readCurveRangeAsync(
                self.__id, int(params["page"]), int(params["pageSize"])
            )
            self.assertEqual(output, self.__curveRangeOutput)

    async def test_readCurveRangeProductAsync(self):
        with responses.RequestsMock() as rsps:
            params = {"page": "1", "pageSize": "2", "product": "PRODUCT"}
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity/" + str(self.__id) + "/curves",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__curveRangeSerializedOutput,
                status=200,
            )
            output = await self.__service.readCurveRangeAsync(
                self.__id,
                int(params["page"]),
                int(params["pageSize"]),
                params["product"],
            )
            self.assertEqual(output, self.__curveRangeOutput)

    async def test_readCurveRangeVersionFromToAsync(self):
        with responses.RequestsMock() as rsps:
            params = {
                "page": "1",
                "pageSize": "2",
                "versionFrom": "2021-03-12T14:30:00",
                "versionTo": "2021-03-16T14:30:00",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity/" + str(self.__id) + "/curves",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__curveRangeSerializedOutput,
                status=200,
            )
            output = await self.__service.readCurveRangeAsync(
                self.__id,
                int(params["page"]),
                int(params["pageSize"]),
                None,
                params["versionFrom"],
                params["versionTo"],
            )
            self.assertEqual(output, self.__curveRangeOutput)

    async def test_checkConversionAsync(self):
        with responses.RequestsMock() as rsps:
            params = {
                "inputUnitsOfMeasure": [CommonUnitOfMeasure.MW, CommonUnitOfMeasure.MWh, CommonUnitOfMeasure.day],
                "targetUnitOfMeasure": CommonUnitOfMeasure.kW,
            }
            rsps.add(
                "GET",
                self.__baseurl + "/uom/checkconversion",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__checkConversionResultSerializedOutput,
                status=200,
            )
            output = await self.__service.checkConversionAsync(
                params["inputUnitsOfMeasure"],
                params["targetUnitOfMeasure"],
            )
            self.assertEqual(output, self.__checkConversionResult)

    async def test_searchFacetAsync(self):
        with responses.RequestsMock() as rsps:
            params = {
                "page": "1",
                "pageSize": "2",
                "searchText": "arktest +curve",
                "filters": {"Market": ["Italy", "France"]},
                "sorts": ["FacetName", "FacetType"],
                "doNotLoadAdditionalInfo": True,
            }
            paramsToMatch = {
                "page": "1",
                "pageSize": "2",
                "searchText": "arktest +curve",
                "filters": ["Market:Italy", "Market:France"],
                "sorts": ["FacetName", "FacetType"],
                "doNotLoadAdditionalInfo": True,
            }

            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/searchfacet",
                match=[responses.matchers.query_param_matcher(paramsToMatch)],
                json=self.__artesianSearchResultsSerializedOutput,
                status=200,
            )
            output = await self.__service.searchFacetAsync(
                int(params["page"]),
                int(params["pageSize"]),
                str(params["searchText"]),
                params["filters"],
                params["sorts"],
                bool(params["doNotLoadAdditionalInfo"]),
            )
            self.assertEqual(output, self.__artesianSearchResults)

    async def test_registerDataQualityRuleAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/dataquality/dqrule",
                match=[
                    responses.matchers.json_params_matcher(
                        self.__dataQualityRuleInputSerialized
                    )
                ],
                json=self.__dataQualityRuleOutputSerialized,
                status=200,
            )

            output = await self.__service.registerDataQualityRuleAsync(
                self.__dataQualityRuleInput
            )

            self.assertEqual(output, self.__dataQualityRuleOutput)

    async def test_readDataQualityRuleByIdAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/dqrule/" + str(self.__id),
                json=self.__dataQualityRuleOutputSerialized,
                status=200,
            )

            output = await self.__service.readDataQualityRuleByIdAsync(self.__id)

            self.assertEqual(output, self.__dataQualityRuleOutput)

    async def test_readDataQualityRuleAsync(self):
        with responses.RequestsMock() as rsps:
            params = {
                "marketDataId": "1",
                "page": "1",
                "pageSize": "10",
                "type": "CompletenessAndFreshness",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/dqrule",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__pagedDataQualityRuleOutputSerialized,
                status=200,
            )

            output = await self.__service.readDataQualityRuleAsync(
                int(params["page"]),
                int(params["pageSize"]),
                RuleType.CompletenessAndFreshness,
                int(params["marketDataId"]),
                "",
                [],
                [],
            )

            self.assertEqual(output, self.__pagedDataQualityRuleOutput)

    async def test_updateDataQualityRuleAsync(self):
        with responses.RequestsMock() as rsps:
            updateInput = DataQualityRuleDtoInput(
                id=1,
                name="TestRuleUpdate",
                type=RuleType.CompletenessAndFreshness,
                configuration=self.__dataQualityRuleConfig,
                version=1,
            )
            rsps.add(
                "PUT",
                self.__baseurl + "/dataquality/dqrule/" + str(self.__id),
                match=[responses.matchers.json_params_matcher(
                    artesianJsonSerialize(updateInput)
                )],
                json=self.__dataQualityRuleOutputSerialized,
                status=200,
            )

            output = await self.__service.updateDataQualityRuleAsync(
                self.__id, updateInput
            )

            self.assertEqual(output, self.__dataQualityRuleOutput)

    async def test_deleteDataQualityRuleAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/dqrule/" + str(self.__id),
                status=204,
            )

            await self.__service.deleteDataQualityRuleAsync(self.__id)

            self.assertEqual(len(rsps.calls), 1)

    async def test_registerDataQualityRuleAssignmentAsync(self):
        with responses.RequestsMock() as rsps:
            params = {"initializationLookbackPeriod": "P30D"}
            rsps.add(
                "POST",
                self.__baseurl + "/dataquality/dqruleassignment",
                match=[
                    responses.matchers.query_param_matcher(params),
                    responses.matchers.json_params_matcher(
                        self.__dataQualityRuleAssignmentInputSerialized
                    ),
                ],
                json=self.__dataQualityRuleAssignmentOutputSerialized,
                status=200,
            )

            output = await self.__service.registerDataQualityRuleAssignmentAsync(
                self.__dataQualityRuleAssignmentInput,
                "P30D",
            )

            self.assertEqual(output, self.__dataQualityRuleAssignmentOutput)

    async def test_readDataQualityRuleAssignmentByIdAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/dqruleassignment/" + str(self.__id),
                json=self.__dataQualityRuleAssignmentOutputSerialized,
                status=200,
            )

            output = await self.__service.readDataQualityRuleAssignmentByIdAsync(
                self.__id
            )

            self.assertEqual(output, self.__dataQualityRuleAssignmentOutput)

    async def test_readDataQualityRuleAssignmentAsync(self):
        with responses.RequestsMock() as rsps:
            sort = ["Id asc"]
            params = {
                "page": "1",
                "pageSize": "10",
                "marketDataId": "100",
                "ruleId": "1",
                "ruleName": "TestRule",
                "sort": "Id asc",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/dqruleassignment",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__pagedDataQualityRuleAssignmentOutputSerialized,
                status=200,
            )

            output = await self.__service.readDataQualityRuleAssignmentAsync(
                int(params["page"]),
                int(params["pageSize"]),
                int(params["marketDataId"]),
                int(params["ruleId"]),
                str(params["ruleName"]),
                sort,
            )

            self.assertEqual(output, self.__pagedDataQualityRuleAssignmentOutput)

    async def test_updateDataQualityRuleAssignmentAsync(self):
        with responses.RequestsMock() as rsps:
            params = {
                "initializationLookbackPeriod": "P60D",
                "etag": "test-etag",
            }
            rsps.add(
                "PUT",
                self.__baseurl + "/dataquality/dqruleassignment/" + str(self.__id),
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__dataQualityRuleAssignmentOutputSerialized,
                status=200,
            )

            output = await self.__service.updateDataQualityRuleAssignmentAsync(
                self.__id,
                "P60D",
                "test-etag",
            )

            self.assertEqual(output, self.__dataQualityRuleAssignmentOutput)

    async def test_deleteDataQualityRuleAssignmentAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/dqruleassignment/" + str(self.__id),
                status=204,
            )

            await self.__service.deleteDataQualityRuleAssignmentAsync(self.__id)

            self.assertEqual(len(rsps.calls), 1)
