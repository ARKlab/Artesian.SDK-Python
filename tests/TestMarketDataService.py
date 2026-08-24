from Artesian import ArtesianConfig
import responses
import unittest
from Artesian.MarketData._Dto.DerivedTransformQueryValidation import DerivedTransformQueryValidation
from Artesian.MarketData._Dto.DerivedTransformQueryValidationResponse import DerivedTransformQueryValidationResponse
from Artesian.MarketData._Dto.TimeSerieData import TimeSerieData
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from datetime import date, datetime
from uuid import UUID
from Artesian.MarketData import (
    ArtesianMetadataFacet,
    ArtesianMetadataFacetCount,
    ArtesianMetadataFacetType,
    ArtesianSearchResults,
    CheckConversionResult,
    CommonUnitOfMeasure,
    DataQualityStatusSummaryDto,
    CurveRangeEntity,
    DerivedAlgorithm,
    DerivedCfg,
    Granularity,
    MarketDataEntityInput,
    MarketDataEntityOutput,
    MarketDataEntityOutputEnriched,
    MarketDataCurveSummaryDto,
    MarketDataService,
    MarketDataTypeV2,
    PagedResultCurveRangeEntity,
    UnitOfMeasure,
    AlertType,
    MarketDataIdentifier,
    OverrideKind,
    OverrideMetadataEntry,
    PagedResultOverrideMetadataEntry,
    UpsertCurveDataOverride,
)
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
from Artesian.MarketData._Enum.RuleType import RuleType
from Artesian.MarketData._Dto.CheckResultExtract import CheckResultExtractVts, CheckResultExtractTs
from Artesian.MarketData._Dto.DqRuleDqStatusSummaryDto import DqRuleDqStatusSummaryDto
from Artesian.MarketData._Dto.MarketDataDqStatusSummaryDto import MarketDataDqStatusSummaryDto
from Artesian.MarketData._Dto.DqCheckChangeEventDto import (
    DqCheckChangeEventDtoOutput,
    LocalDateTimeRange,
)
from Artesian.MarketData._Enum.CheckAggregatedStatus import CheckAggregatedStatus
from Artesian.MarketData._Dto.AlertScheduleEventsDto import AlertScheduleEventsDtoOutput
from Artesian.MarketData._Dto.MailNotificationDto import MailNotificationDto
from Artesian.MarketData._Dto.PagedResult import PagedResultQualityNotificationAlertDtoOutput
from Artesian.MarketData._Dto.PagedResult import (
    PagedResultQualityNotificationAlertAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoInput,
    QualityNotificationAlertDtoOutput,
)
from Artesian.MarketData._Dto.QualityNotificationAlertAssignmentDto import (
    QualityNotificationAlertAssignmentDtoInput,
    QualityNotificationAlertAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.TriggerConfigDto import TriggerConfigDto

cfg = ArtesianConfig("https://baseurl.com", "APIKey")


class AlertTriggerConfigFixture(TriggerConfigDto):
    @property
    def type(self: "AlertTriggerConfigFixture") -> AlertType:
        return AlertType.OnEvent

    def __eq__(self: "AlertTriggerConfigFixture", other: object) -> bool:
        return isinstance(other, AlertTriggerConfigFixture)


class TestMarketDataServiceMarketData(unittest.IsolatedAsyncioTestCase):
    def setUp(self: "TestMarketDataServiceMarketData") -> None:
        self.__service = MarketDataService(cfg)
        QualityNotificationAlertDtoInput.__init__.__annotations__["triggerConfig"] = (
            AlertTriggerConfigFixture
        )
        QualityNotificationAlertDtoOutput.__init__.__annotations__["triggerConfig"] = (
            AlertTriggerConfigFixture
        )

        curveIds = [1, 2]
        derivedCfg = DerivedCfg(
                        version=1,
                        derivedAlgorithm=DerivedAlgorithm.Coalesce,
                        orderedReferencedMarketDataIds=curveIds,
                    )

        derivedCfgTransform = DerivedCfg(
                        version=1,
                        derivedAlgorithm=DerivedAlgorithm.Transform,
                        orderedReferencedMarketDataIds=[1000],
                        transform="SELECT Time, (Value + 1) as Value FROM $table",
                    )

        self.__sampleOutput = MarketDataEntityOutput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataTypeV2.ActualTimeSerie,
            originalTimezone="CET",
            tags={"PythonTag": ["PythonTagValue1", "PythonTagValue2"]},
            derivedCfg=derivedCfg,
            unitOfMeasure=UnitOfMeasure(value=CommonUnitOfMeasure.MW)
        )
        self.__sampleOutputEnriched = MarketDataEntityOutputEnriched(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataTypeV2.ActualTimeSerie,
            originalTimezone="CET",
            tags={"PythonTag": ["PythonTagValue1", "PythonTagValue2"]},
            derivedCfg=derivedCfg,
            unitOfMeasure=UnitOfMeasure(value=CommonUnitOfMeasure.MW),
            dataQualityStatusSummary={
                "CompletenessAndFreshness": DataQualityStatusSummaryDto(
                    lastCheckTime=datetime(2024, 1, 3, 12, 0),
                    overallStatus=CheckAggregatedStatus.OK,
                    activeRulesCount=1,
                    failedRulesCount=0,
                    from_=date(2024, 1, 1),
                    to=date(2024, 1, 3),
                )
            },
            curveSummary=MarketDataCurveSummaryDto(
                dataLastWritedAt=datetime(2024, 1, 3, 12, 0),
                dataRangeStart=date(2024, 1, 1),
                dataRangeEnd=date(2024, 1, 3),
            ),
        )
        self.__serializedOutputEnriched = artesianJsonSerialize(
            self.__sampleOutputEnriched
        )
        self.__serializedOutput = artesianJsonSerialize(self.__sampleOutput)
        self.__sampleInput = MarketDataEntityInput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataTypeV2.ActualTimeSerie,
            originalTimezone="CET",
            tags={"PythonTag": ["PythonTagValue1", "PythonTagValue2"]},
            derivedCfg=derivedCfg,
            unitOfMeasure=UnitOfMeasure(value=CommonUnitOfMeasure.MW)
        )
        self.__sampleOutputTransform = MarketDataEntityOutput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataTypeV2.ActualTimeSerie,
            originalTimezone="CET",
            derivedCfg=derivedCfgTransform
        )
        self.__serializedOutputTransform = artesianJsonSerialize(self.__sampleOutputTransform)
        self.__sampleInputTransform = MarketDataEntityInput(
            providerName="PROVIDER",
            marketDataName="MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataTypeV2.ActualTimeSerie,
            originalTimezone="CET",
            derivedCfg=derivedCfgTransform
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
            results=[self.__sampleOutputEnriched],
            facets=[self.__artesianMetadataFacet],
            countResults=1,
        )
        self.__artesianSearchResultsSerializedOutput = artesianJsonSerialize(
            self.__artesianSearchResults
        )
        self.__checkConversionResult = CheckConversionResult(
            targetUnitOfMeasure=CommonUnitOfMeasure.kW,
            convertibleInputUnitsOfMeasure=[CommonUnitOfMeasure.MW, CommonUnitOfMeasure.MWh],
            notConvertibleInputUnitsOfMeasure=[CommonUnitOfMeasure.day]
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
        self.__derivedTransformQueryValidationResponse = DerivedTransformQueryValidationResponse(
            data=TimeSerieData(
                    rows={
                        datetime(2020, 1, 1, 1): 42.0,
                        datetime(2020, 1, 2, 2): 43.0,
                    },
                    type=MarketDataTypeV2.ActualTimeSerie
                ),
            valid=True
        )
        self.__derivedTransformQueryValidationResponseSerializedOutput = artesianJsonSerialize(
            self.__derivedTransformQueryValidationResponse
        )
        self.__sampleVts = CheckResultExtractVts(
            time=datetime(2024, 1, 15, 10, 0),
            issueCount=5,
            competenceStart=datetime(2024, 1, 1),
            competenceEnd=datetime(2024, 1, 31),
            providerName="PROVIDER",
            curveName="CURVE",
            ruleName="RULE",
            assignmentId=1,
            marketDataId=100,
            ruleId=1,
            version=datetime(2024, 1, 15, 10, 0),
        )
        self.__sampleTs = CheckResultExtractTs(
            time=datetime(2024, 1, 15, 10, 0),
            issueCount=3,
            competenceStart=datetime(2024, 1, 1),
            competenceEnd=datetime(2024, 1, 31),
            providerName="PROVIDER",
            curveName="CURVE",
            ruleName="RULE",
            assignmentId=3,
            marketDataId=200,
            ruleId=2,
        )
        self.__sampleMdDq = MarketDataDqStatusSummaryDto(marketDataId=100)
        self.__sampleDqRule = DqRuleDqStatusSummaryDto(ruleId=1)

        self.__qualityNotificationAlertInput = QualityNotificationAlertDtoInput(
            name="Weather station daily digest",
            triggerConfig=AlertTriggerConfigFixture(),
            mailNotifications=[MailNotificationDto(recipients=["alerts@example.com"])],
            version=0,
        )
        self.__qualityNotificationAlertOutput = QualityNotificationAlertDtoOutput(
            name="Weather station daily digest",
            triggerConfig=AlertTriggerConfigFixture(),
            id=self.__id,
            mailNotifications=[MailNotificationDto(recipients=["alerts@example.com"])],
            eTag="alert-etag-1",
            version=1,
        )
        self.__qualityNotificationAlertInputSerialized = artesianJsonSerialize(
            self.__qualityNotificationAlertInput
        )
        self.__qualityNotificationAlertOutputSerialized = artesianJsonSerialize(
            self.__qualityNotificationAlertOutput
        )
        self.__pagedQualityNotificationAlertOutput = (
            PagedResultQualityNotificationAlertDtoOutput(
                1, 10, 1, False, [self.__qualityNotificationAlertOutput]
            )
        )
        self.__pagedQualityNotificationAlertOutputSerialized = artesianJsonSerialize(
            self.__pagedQualityNotificationAlertOutput
        )

        return super().setUp()

    async def test_registerMarketData(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_registerMarketDataTransform(self: "TestMarketDataServiceMarketData") -> None:
        expectedJson = {
            "MarketDataId": 0,
            "ProviderName": "PROVIDER",
            "MarketDataName": "MARKETDATA",
            "OriginalGranularity": "Day",
            "Type": "ActualTimeSerie",
            "OriginalTimezone": "CET",
            "AggregationRule": "Undefined",
            "DerivedCfg":
            {
                "DerivedAlgorithm": "Transform",
                "Version": 1,
                "OrderedReferencedMarketDataIds": [1000],
                "Transform": "SELECT Time, (Value + 1) as Value FROM $table"
            }
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/entity",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                json=self.__serializedOutputTransform,
                status=200,
            )

            output = await self.__service.registerMarketDataAsync(self.__sampleInputTransform)

            self.assertEqual(output, self.__sampleOutputTransform)

    async def test_readMarketDataRegistryByNameAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "provider": "PROVIDER",
                "curveName": "MARKETDATA",
                "includeCurveSummary": True,
                "includeTimeTransform": True,
                "includeDataQuality": False,
                "skipOverrides": False,
            }
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__serializedOutput,
                status=200,
            )
            output = await self.__service.readMarketDataRegistryByNameAsync(
                params["provider"],
                params["curveName"],
                params["includeCurveSummary"],
                params["includeTimeTransform"],
                params["includeDataQuality"],
                params["skipOverrides"],
            )
            self.assertEqual(output, self.__sampleOutput)

    async def test_deleteMarketDataAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/marketdata/entity/" + str(self.__id),
                status=204,
            )
            await self.__service.deleteMarketDataAsync(self.__id)
            self.assertEqual(len(rsps.calls), 1)

    async def test_updateMarketDataAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readMarketDataRegistryByIdAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "includeCurveSummary": True,
                "includeTimeTransform": True,
                "includeDataQuality": False,
                "skipOverrides": False,
            }
            rsps.add(
                "GET",
                self.__baseurl + "/marketdata/entity/" + str(self.__id),
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__serializedOutput,
                status=200,
            )
            output = await self.__service.readMarketDataRegistryByIdAsync(
                self.__id,
                params["includeCurveSummary"],
                params["includeTimeTransform"],
                params["includeDataQuality"],
                params["skipOverrides"],
            )
            self.assertEqual(output, self.__sampleOutput)

    async def test_readCurveRangePaginationAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readCurveRangeProductAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readCurveRangeVersionFromToAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_checkConversionAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_derivedTransformQueryValidationAsync(self: "TestMarketDataServiceMarketData") -> None:
        expectedJson = {
            "Data": {
                "Rows": [
                    {"Key": "2020-01-01T01:00:00.000000", "Value": 42.0},
                    {"Key": "2020-01-02T02:00:00.000000", "Value": 43.0},
                ],
                "Type": "ActualTimeSerie"
            },
            "Transform": "SELECT Time, (Value + 1) as Value FROM $table",
        }
        derivedValidation = DerivedTransformQueryValidation(
            data=TimeSerieData(
                    rows={
                        datetime(2020, 1, 1, 1): 42.0,
                        datetime(2020, 1, 2, 2): 43.0,
                    },
                    type=MarketDataTypeV2.ActualTimeSerie
                ),
            transform="SELECT Time, (Value + 1) as Value FROM $table"
        )
        ser = artesianJsonSerialize(derivedValidation)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/utils/derivedTransform/queryValidation",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                json=self.__derivedTransformQueryValidationResponseSerializedOutput,
                status=200,
            )

            output = await self.__service.derivedTransformQueryValidationAsync(derivedValidation)

            self.assertEqual(output, self.__derivedTransformQueryValidationResponse)

    async def test_searchFacetAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "page": "1",
                "pageSize": "2",
                "searchText": "arktest +curve",
                "filters": {"Market": ["Italy", "France"]},
                "sorts": ["FacetName", "FacetType"],
                "doNotLoadAdditionalInfo": True,
                "includeCurveSummary": True,
                "includeTimeTransform": True,
                "includeDataQuality": False,
                "skipOverrides": False,
            }
            paramsToMatch = {
                "page": "1",
                "pageSize": "2",
                "searchText": "arktest +curve",
                "filters": ["Market:Italy", "Market:France"],
                "sorts": ["FacetName", "FacetType"],
                "doNotLoadAdditionalInfo": True,
                "includeCurveSummary": True,
                "includeTimeTransform": True,
                "includeDataQuality": False,
                "skipOverrides": False,
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
                bool(params["includeCurveSummary"]),
                bool(params["includeTimeTransform"]),
                bool(params["includeDataQuality"]),
                bool(params["skipOverrides"]),
            )
            self.assertEqual(output, self.__artesianSearchResults)

    async def test_registerDataQualityRuleAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readDataQualityRuleByIdAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/dqrule/" + str(self.__id),
                json=self.__dataQualityRuleOutputSerialized,
                status=200,
            )

            output = await self.__service.readDataQualityRuleByIdAsync(self.__id)

            self.assertEqual(output, self.__dataQualityRuleOutput)

    async def test_readDataQualityRuleAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_updateDataQualityRuleAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_deleteDataQualityRuleAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/dqrule/" + str(self.__id),
                status=204,
            )

            await self.__service.deleteDataQualityRuleAsync(self.__id)

            self.assertEqual(len(rsps.calls), 1)

    async def test_registerQualityNotificationAlertAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/dataquality/alertrule",
                match=[
                    responses.matchers.json_params_matcher(
                        self.__qualityNotificationAlertInputSerialized
                    )
                ],
                json=self.__qualityNotificationAlertOutputSerialized,
                status=200,
            )

            output = await self.__service.registerQualityNotificationAlertAsync(
                self.__qualityNotificationAlertInput
            )

            self.assertEqual(output, self.__qualityNotificationAlertOutput)

    async def test_readQualityNotificationAlertByIdAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertrule/" + str(self.__id),
                json=self.__qualityNotificationAlertOutputSerialized,
                status=200,
            )

            output = await self.__service.readQualityNotificationAlertByIdAsync(
                self.__id
            )

            self.assertEqual(output, self.__qualityNotificationAlertOutput)

    async def test_readQualityNotificationAlertsAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "name": "Weather",
                "marketDataId": "100",
                "page": "1",
                "pageSize": "10",
                "ruleIds": ["1", "2"],
                "sort": "Name asc",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertrule",
                match=[responses.matchers.query_param_matcher(params)],
                json=self.__pagedQualityNotificationAlertOutputSerialized,
                status=200,
            )

            output = await self.__service.readQualityNotificationAlertsAsync(
                1, 10, "Weather", 100, [1, 2], ["Name asc"]
            )

            self.assertEqual(output, self.__pagedQualityNotificationAlertOutput)

    async def test_updateQualityNotificationAlertAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "PUT",
                self.__baseurl + "/dataquality/alertrule/" + str(self.__id),
                match=[
                    responses.matchers.json_params_matcher(
                        self.__qualityNotificationAlertInputSerialized
                    )
                ],
                json=self.__qualityNotificationAlertOutputSerialized,
                status=200,
            )

            output = await self.__service.updateQualityNotificationAlertAsync(
                self.__id, self.__qualityNotificationAlertInput
            )

            self.assertEqual(output, self.__qualityNotificationAlertOutput)

    async def test_deleteQualityNotificationAlertAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/alertrule/" + str(self.__id),
                status=204,
            )

            await self.__service.deleteQualityNotificationAlertAsync(self.__id)

            self.assertEqual(len(rsps.calls), 1)

    async def test_readAlertScheduleEventsAsync(self: "TestMarketDataServiceMarketData") -> None:
        scheduleTime = datetime(2024, 1, 15, 10, 0)
        scheduleEvents = AlertScheduleEventsDtoOutput(scheduleTime=scheduleTime)
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl
                + "/dataquality/alertrule/1/schedule/2024-01-15T10:00:00/events",
                json=artesianJsonSerialize(scheduleEvents),
                status=200,
            )

            output = await self.__service.readAlertScheduleEventsAsync(
                self.__id, scheduleTime
            )

            self.assertEqual(output, scheduleEvents)

    async def test_readAlertScheduleListAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertrule/1/schedule",
                match=[responses.matchers.query_param_matcher({"lastN": "3"})],
                json=["2024-01-15T10:00:00", "2024-01-14T10:00:00"],
                status=200,
            )

            output = await self.__service.readAlertScheduleListAsync(self.__id, 3)

            self.assertEqual(
                output,
                [datetime(2024, 1, 15, 10, 0), datetime(2024, 1, 14, 10, 0)],
            )

    async def test_readAlertScheduleLastEventsAsync(self: "TestMarketDataServiceMarketData") -> None:
        scheduleEvents = AlertScheduleEventsDtoOutput()
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertrule/1/schedule/latest/events",
                json=artesianJsonSerialize(scheduleEvents),
                status=200,
            )

            output = await self.__service.readAlertScheduleLastEventsAsync(self.__id)

            self.assertEqual(output, scheduleEvents)

    async def test_registerQualityNotificationAlertAssignmentAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        entity = QualityNotificationAlertAssignmentDtoInput(
            alertId=1,
            marketDataId=100,
        )
        expected = QualityNotificationAlertAssignmentDtoOutput(
            id=1,
            alertId=1,
            marketDataId=100,
            eTag="assignment-etag-1",
        )

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/dataquality/alertruleassignment",
                match=[
                    responses.matchers.json_params_matcher(
                        artesianJsonSerialize(entity)
                    )
                ],
                json=artesianJsonSerialize(expected),
                status=200,
            )

            output = await self.__service.registerQualityNotificationAlertAssignmentAsync(
                entity
            )

            self.assertEqual(output, expected)

    async def test_readQualityNotificationAlertAssignmentByIdAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        expected = QualityNotificationAlertAssignmentDtoOutput(
            id=1,
            alertId=1,
            marketDataId=100,
        )

        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertruleassignment/1",
                json=artesianJsonSerialize(expected),
                status=200,
            )

            output = await self.__service.readQualityNotificationAlertAssignmentByIdAsync(
                1
            )

            self.assertEqual(output, expected)

    async def test_readQualityNotificationAlertAssignmentsAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        assignment = QualityNotificationAlertAssignmentDtoOutput(
            id=1,
            alertId=1,
            marketDataId=100,
        )
        expected = PagedResultQualityNotificationAlertAssignmentDtoOutput(
            1, 10, 1, False, [assignment]
        )
        params = {
            "alertId": "1",
            "marketDataId": "100",
            "page": "1",
            "pageSize": "10",
            "sort": "Id asc",
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/alertruleassignment",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize(expected),
                status=200,
            )

            output = await self.__service.readQualityNotificationAlertAssignmentsAsync(
                1, 10, 1, 100, ["Id asc"]
            )

            self.assertEqual(output, expected)

        with self.assertRaises(ValueError):
            await self.__service.readQualityNotificationAlertAssignmentsAsync(0, 10)

        with self.assertRaises(ValueError):
            await self.__service.readQualityNotificationAlertAssignmentsAsync(1, 0)

    async def test_deleteQualityNotificationAlertAssignmentAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/alertruleassignment/1",
                status=204,
            )

            await self.__service.deleteQualityNotificationAlertAssignmentAsync(1)

            self.assertEqual(len(rsps.calls), 1)

    async def test_registerDataQualityRuleAssignmentAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readDataQualityRuleAssignmentByIdAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_readDataQualityRuleAssignmentAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_updateDataQualityRuleAssignmentAsync(self: "TestMarketDataServiceMarketData") -> None:
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

    async def test_deleteDataQualityRuleAssignmentAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            rsps.add(
                "DELETE",
                self.__baseurl + "/dataquality/dqruleassignment/" + str(self.__id),
                status=204,
            )

            await self.__service.deleteDataQualityRuleAssignmentAsync(self.__id)

            self.assertEqual(len(rsps.calls), 1)

    async def test_readDataQualityRuleAssignmentEventsFeedAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        afterTimestamp = datetime(2024, 1, 15, 10, 0)
        event = DqCheckChangeEventDtoOutput(
            marketDataId=100,
            ruleId=1,
            assignmentId=self.__id,
            rangeImpacted=LocalDateTimeRange(
                start=datetime(2024, 1, 15),
                end=datetime(2024, 1, 16),
            ),
            newStatus=CheckAggregatedStatus.KO,
            oldStatus=CheckAggregatedStatus.OK,
            timestamp=datetime(2024, 1, 15, 10, 0),
            ruleName="TestRule",
            ruleVersion=2,
            marketDataName="TestMarketData",
            provider="TestProvider",
        )
        params = {"afterTimestamp": "2024-01-15T10:00:00"}

        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl
                + "/dataquality/dqruleassignment/1/events",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize([event]),
                status=200,
            )

            output = await self.__service.readDataQualityRuleAssignmentEventsFeedAsync(
                self.__id,
                afterTimestamp,
            )

            self.assertEqual(output, [event])

    async def test_getDataQualityCheckResultExtractVtsAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "timeZone": "UTC",
                "assignmentIds": ["1", "2"],
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/checkresult/extract/vts/Version/2024-01-15T10:00:00/"
                "Day/2024-01-01/2024-01-31",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize([self.__sampleVts]),
                status=200,
            )
            output = await self.__service.getDataQualityCheckResultExtractVtsAsync(
                version="2024-01-15T10:00:00",
                granularity="Day",
                start="2024-01-01",
                end="2024-01-31",
                timeZone="UTC",
                assignmentIds=[1, 2],
            )
            self.assertEqual(output, [self.__sampleVts])

    async def test_getDataQualityCheckResultExtractTsAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "timeZone": "Europe/Rome",
                "assignmentIds": ["3", "4"],
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/checkresult/extract/ts/Hour/2024-01-01/2024-01-31",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize([self.__sampleTs]),
                status=200,
            )
            output = await self.__service.getDataQualityCheckResultExtractTsAsync(
                granularity="Hour",
                start="2024-01-01",
                end="2024-01-31",
                timeZone="Europe/Rome",
                assignmentIds=[3, 4],
            )
            self.assertEqual(output, [self.__sampleTs])

    async def test_getDataQualityCheckResultCheckSummaryAsync(self: "TestMarketDataServiceMarketData") -> None:
        from Artesian.MarketData._Dto.PagedResult import PagedResultCheckResultCheckSummaryDto
        expectedOutput = PagedResultCheckResultCheckSummaryDto(page=1, pageSize=20, count=0,
                                                               isCountPartial=False, data=[])
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/checkresult/checksummary",
                json={"page": 1, "pageSize": 20, "count": 0, "isCountPartial": False, "data": []},
                status=200,
            )
            output = await self.__service.getDataQualityCheckResultCheckSummaryAsync(
                page=1,
                pageSize=20,
                marketDataIds=[100, 200],
                ruleIds=[1, 2],
                assignmentIds=[10, 20],
                dqStatus=CheckAggregatedStatus.KO,
                from_date="2024-01-01T00:00:00",
                to_date="2024-01-31T23:59:00",
                versionFrom="2024-01-01T00:00:00",
                versionTo="2024-01-31T23:59:00",
                products=["PROD1", "PROD2"],
                skipEmptyRanges=True,
                sort=["RuleName asc"],
            )
            self.assertEqual(output, expectedOutput)

    async def test_getMarketDataDqStatusSummaryAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "limit": "50",
                "ruleId": "1",
                "marketDataIds": ["100", "200"],
                "dqStatus": "KO",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/checkresult/marketdata/dataqualitystatussummary",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize([self.__sampleMdDq]),
                status=200,
            )
            output = await self.__service.getMarketDataDqStatusSummaryAsync(
                ruleId=1,
                marketDataIds=[100, 200],
                dqStatus=CheckAggregatedStatus.KO,
                limit=50,
            )
            self.assertEqual(output, [self.__sampleMdDq])

    async def test_getDqRuleDqStatusSummaryAsync(self: "TestMarketDataServiceMarketData") -> None:
        with responses.RequestsMock() as rsps:
            params = {
                "limit": "100",
                "marketDataId": "100",
                "ruleIds": ["1", "2", "3"],
                "dqStatus": "OK",
            }
            rsps.add(
                "GET",
                self.__baseurl + "/dataquality/checkresult/dqrule/dataqualitystatussummary",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize([self.__sampleDqRule]),
                status=200,
            )
            output = await self.__service.getDqRuleDqStatusSummaryAsync(
                marketDataId=100,
                ruleIds=[1, 2, 3],
                dqStatus=CheckAggregatedStatus.OK,
                limit=100,
            )
            self.assertEqual(output, [self.__sampleDqRule])

    async def test_upsertCurveDataOverrideAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        betaBaseUrl = "https://baseurl.com/v2.2-beta"
        data = UpsertCurveDataOverride(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "UTC",
            rows={datetime(2020, 1, 1): 42.0},
            kind=OverrideKind.Override,
            comment="test override",
        )
        expected = [
            OverrideMetadataEntry(
                id=UUID("11111111-1111-1111-1111-111111111111"),
                marketDataId=100,
                kind=OverrideKind.Override,
                version=None,
                product=None,
                referencedMarketDataId=100,
                rangeExactStart=datetime(2020, 1, 1),
                rangeExactEnd=datetime(2020, 1, 2),
                createdBy="test-user",
                createdAt=datetime(2020, 1, 1),
            )
        ]

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                betaBaseUrl + "/marketdata/override/upsertdata",
                match=[
                    responses.matchers.json_params_matcher(
                        artesianJsonSerialize(data)
                    )
                ],
                json=artesianJsonSerialize(expected),
                status=200,
            )

            output = await self.__service.upsertCurveDataOverrideAsync(data)

            self.assertEqual(output, expected)

    async def test_deleteOverrideDataAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        betaBaseUrl = "https://baseurl.com/v2.2-beta"
        overrideId = UUID("11111111-1111-1111-1111-111111111111")

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                betaBaseUrl
                + "/marketdata/override/"
                + str(overrideId)
                + "/deletedata",
                status=204,
            )

            await self.__service.deleteOverrideDataAsync(overrideId)

            self.assertEqual(len(rsps.calls), 1)

    async def test_readOverrideMetadataAsync(
        self: "TestMarketDataServiceMarketData",
    ) -> None:
        betaBaseUrl = "https://baseurl.com/v2.2-beta"
        expected = PagedResultOverrideMetadataEntry(
            page=2,
            pageSize=5,
            count=1,
            isCountPartial=False,
            data=[
                OverrideMetadataEntry(
                    id=UUID("11111111-1111-1111-1111-111111111111"),
                    marketDataId=100,
                    kind=OverrideKind.Fallback,
                    version=None,
                    product=None,
                    referencedMarketDataId=100,
                    rangeExactStart=datetime(2020, 1, 1),
                    rangeExactEnd=datetime(2020, 1, 2),
                    createdBy="test-user",
                    createdAt=datetime(2020, 1, 1),
                )
            ],
        )
        params = {"kind": "Fallback", "page": "2", "pageSize": "5"}

        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                betaBaseUrl + "/marketdata/override/100/metadata",
                match=[responses.matchers.query_param_matcher(params)],
                json=artesianJsonSerialize(expected),
                status=200,
            )

            output = await self.__service.readOverrideMetadataAsync(
                100,
                OverrideKind.Fallback,
                2,
                5,
            )

            self.assertEqual(output, expected)
