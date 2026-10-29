from __future__ import annotations

import unittest
from datetime import date, datetime
from typing import cast

from Artesian._ClientsExecutor.ArtesianJsonSerializer import (
    artesianJsonDecode,
    artesianJsonDeserialize,
    artesianJsonEncode,
    artesianJsonSerialize,
)
from Artesian.MarketData import (
    ActualCompletenessAndFreshnessConfigDto,
    BidAskCompletenessAndFreshnessConfigDto,
    BidAskDataQualityField,
    BidAskOutlierConfigDto,
    CheckResultExtractBidAsk,
    CheckResultExtractMas,
    CronScheduleDefinitionDto,
    DataQualityStatusSummaryDto,
    MasCompletenessAndFreshnessConfigDto,
    MasDataQualityField,
    MasOutlierConfigDto,
    OnEventTriggerConfigDto,
    OutlierAbsoluteBoundConfigDto,
    OutlierConfigDto,
    OutlierRefCurveConfigDto,
    ScheduleConfigDto,
    ScheduleTriggerConfigDto,
    VersionedCompletenessAndFreshnessConfigDto,
)
from Artesian.MarketData._Dto.AlertScheduleEventsDto import AlertScheduleEventsDtoOutput
from Artesian.MarketData._Dto.CheckResultExtract import (
    CheckResultExtractTs,
    CheckResultExtractVts,
)
from Artesian.MarketData._Dto.DataQualityRuleConfigDto import DataQualityRuleConfigDto
from Artesian.MarketData._Dto.DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from Artesian.MarketData._Dto.DqCheckChangeEventDto import (
    DqCheckChangeEventDtoOutput,
    LocalDateTimeRange,
)
from Artesian.MarketData._Dto.OutlierModelConfigDto import OutlierModelConfigDto
from Artesian.MarketData._Dto.PagedResult import PagedResultDqCheckChangeEventDtoOutput
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoOutput,
)
from Artesian.MarketData._Dto.RecordValidationConfigDto import RecordValidationConfigDto
from Artesian.MarketData._Dto.ScheduleDefinitionDto import ScheduleDefinitionDto
from Artesian.MarketData._Dto.TriggerConfigDto import TriggerConfigDto
from Artesian.MarketData._Enum.CheckAggregatedStatus import CheckAggregatedStatus
from Artesian.MarketData._Enum.MarketDataType import MarketDataType
from Artesian.MarketData._Enum.PeriodPrecision import PeriodPrecision


class TestDataQualitySerialization(unittest.TestCase):
    def test_compact_extract_ts_round_trip(
        self: TestDataQualitySerialization,
    ) -> None:
        payload = {
            "P": "provider",
            "C": "curve",
            "R": "rule",
            "AID": 3,
            "MKID": 4,
            "RID": 5,
            "T": "2024-01-01T00:00:00",
            "D": 2,
            "S": "2024-01-01T00:00:00",
            "E": "2024-01-02T00:00:00",
        }

        result = artesianJsonDeserialize(payload, CheckResultExtractTs)

        self.assertEqual(result.assignmentId, 3)
        self.assertEqual(artesianJsonSerialize(result), payload)

    def test_compact_extract_vts_uses_version_key(
        self: TestDataQualitySerialization,
    ) -> None:
        result = CheckResultExtractVts(
            time=datetime(2024, 1, 1),
            issueCount=2,
            competenceStart=datetime(2024, 1, 1),
            competenceEnd=datetime(2024, 1, 2),
            version=datetime(2023, 12, 31),
        )

        payload = artesianJsonSerialize(result)

        self.assertEqual(payload["V"], "2023-12-31T00:00:00")
        self.assertNotIn("Version", payload)

    def test_compact_extract_mas_and_bidask_include_product(
        self: TestDataQualitySerialization,
    ) -> None:
        for resultType in (CheckResultExtractMas, CheckResultExtractBidAsk):
            result = resultType(
                time=datetime(2024, 1, 1),
                issueCount=1,
                competenceStart=datetime(2024, 1, 1),
                competenceEnd=datetime(2024, 1, 2),
                product="GME_D",
            )
            with self.subTest(resultType=resultType):
                payload = artesianJsonSerialize(result)

                self.assertEqual(payload["PR"], "GME_D")
                self.assertEqual(artesianJsonDeserialize(payload, resultType), result)

    def test_rule_configuration_is_deserialized_to_concrete_types(
        self: TestDataQualitySerialization,
    ) -> None:
        actualPayload = {
            "Id": 1,
            "Name": "actual",
            "Type": "CompletenessAndFreshness",
            "Configuration": {
                "Type": "CompletenessAndFreshness",
                "MarketDataType": "ActualTimeSerie",
                "ScheduleConfig": {
                    "ScheduleDefinition": {
                        "Type": "Cron",
                        "CronExpression": "0 0 * * *",
                        "TimeZone": "UTC",
                    },
                    "MaxDelay": "PT1H",
                },
                "RecordValidationConfig": {
                    "RecordRangeFrom": "PT0S",
                    "RecordRangeTo": "PT1H",
                },
            },
            "Version": 1,
        }
        outlierPayload = {
            "Id": 2,
            "Name": "outlier",
            "Type": "Outlier",
            "Configuration": {
                "Type": "Outlier",
                "Model": {
                    "Type": "Outlier",
                    "Model": "AbsoluteBound",
                    "UpperBound": 10.0,
                    "LowerBound": -10.0,
                },
            },
            "Version": 1,
        }

        actual = artesianJsonDeserialize(actualPayload, DataQualityRuleDtoOutput)
        outlier = artesianJsonDeserialize(outlierPayload, DataQualityRuleDtoOutput)

        self.assertIsInstance(actual.configuration, ActualCompletenessAndFreshnessConfigDto)
        schedule_definition = cast(
            CronScheduleDefinitionDto,
            actual.configuration.scheduleConfig.scheduleDefinition,
        )
        self.assertEqual(schedule_definition.cronExpression, "0 0 * * *")
        self.assertIsInstance(outlier.configuration, OutlierConfigDto)
        self.assertIsInstance(outlier.configuration.model, OutlierAbsoluteBoundConfigDto)

    def test_alert_trigger_is_deserialized_to_concrete_type(
        self: TestDataQualitySerialization,
    ) -> None:
        scheduledPayload = {
            "Name": "digest",
            "TriggerConfig": {
                "Type": "Scheduled",
                "ScheduleDefinition": {
                    "Type": "Cron",
                    "CronExpression": "0 8 * * *",
                    "TimeZone": "UTC",
                },
            },
            "Version": 1,
        }
        onEventPayload = {
            "Name": "immediate",
            "TriggerConfig": {"Type": "OnEvent"},
            "Version": 1,
        }

        scheduled = artesianJsonDeserialize(scheduledPayload, QualityNotificationAlertDtoOutput)
        onEvent = artesianJsonDeserialize(onEventPayload, QualityNotificationAlertDtoOutput)

        self.assertIsInstance(scheduled.triggerConfig, ScheduleTriggerConfigDto)
        self.assertIsInstance(onEvent.triggerConfig, OnEventTriggerConfigDto)

    def test_status_summary_maps_from_api_field(
        self: TestDataQualitySerialization,
    ) -> None:
        payload = {"From": "2024-01-01", "To": "2024-01-02"}

        result = artesianJsonDeserialize(payload, DataQualityStatusSummaryDto)

        self.assertEqual(result.from_, date(2024, 1, 1))
        self.assertEqual(artesianJsonSerialize(result)["From"], "2024-01-01")

    def test_status_summary_from_round_trip_and_null_omitted(
        self: TestDataQualitySerialization,
    ) -> None:
        summary = DataQualityStatusSummaryDto(from_=date(2024, 1, 1), to=date(2024, 1, 2))

        payload = artesianJsonSerialize(summary)

        self.assertEqual(payload["From"], "2024-01-01")
        self.assertNotIn("From_", payload)
        self.assertNotIn("from_", payload)
        self.assertEqual(artesianJsonDeserialize(payload, DataQualityStatusSummaryDto), summary)
        self.assertNotIn("From", artesianJsonSerialize(DataQualityStatusSummaryDto()))


class TestPolymorphicSerialization(unittest.TestCase):
    @staticmethod
    def _schedule() -> ScheduleConfigDto:
        return ScheduleConfigDto(
            scheduleDefinition=CronScheduleDefinitionDto(cronExpression="0 0 * * *", timeZone="UTC"),
            maxDelay="PT1H",
        )

    def test_rule_config_round_trips_to_concrete_types(self: TestPolymorphicSerialization) -> None:
        samples: list[DataQualityRuleConfigDto] = [
            ActualCompletenessAndFreshnessConfigDto(
                marketDataType=MarketDataType.ActualTimeSerie,
                scheduleConfig=self._schedule(),
                recordValidationConfig=RecordValidationConfigDto(recordRangeFrom="PT0S", recordRangeTo="PT1H"),
            ),
            VersionedCompletenessAndFreshnessConfigDto(
                marketDataType=MarketDataType.VersionedTimeSerie,
                scheduleConfig=self._schedule(),
                recordValidationConfig=RecordValidationConfigDto(
                    recordRangeFrom="PT0S", recordRangeTo="PT1H", precision=PeriodPrecision.Day
                ),
                versionToleranceFrom="PT0S",
                versionToleranceTo="PT2H",
                versionPrecision=PeriodPrecision.Hour,
            ),
            OutlierConfigDto(model=OutlierAbsoluteBoundConfigDto(upperBound=10.0, lowerBound=-10.0)),
            OutlierConfigDto(model=OutlierRefCurveConfigDto(referenceMarketDataId=7, tolerancePerc=5.0)),
        ]
        for sample in samples:
            with self.subTest(type(sample).__name__, model=getattr(sample, "model", None)):
                payload = artesianJsonSerialize(sample)

                result = artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

                self.assertIs(type(result), type(sample))
                self.assertEqual(result, sample)

    def test_mas_and_bidask_rule_configurations_round_trip(self: TestPolymorphicSerialization) -> None:
        samples: list[
            MasCompletenessAndFreshnessConfigDto
            | BidAskCompletenessAndFreshnessConfigDto
            | MasOutlierConfigDto
            | BidAskOutlierConfigDto
        ] = [
            MasCompletenessAndFreshnessConfigDto(
                scheduleConfig=self._schedule(),
                recordValidationConfig=RecordValidationConfigDto(recordRangeFrom="PT0S", recordRangeTo="PT1H"),
                products=["GME_D"],
                fieldsToBeValidated=[MasDataQualityField.Settlement],
            ),
            BidAskCompletenessAndFreshnessConfigDto(
                scheduleConfig=self._schedule(),
                recordValidationConfig=RecordValidationConfigDto(recordRangeFrom="PT0S", recordRangeTo="PT1H"),
                products=["GME_D"],
                fieldsToBeValidated=[BidAskDataQualityField.BestBidPrice],
            ),
            MasOutlierConfigDto(
                model=OutlierAbsoluteBoundConfigDto(upperBound=10.0, lowerBound=-10.0),
                products=["GME_D"],
                fieldsToBeValidated=[MasDataQualityField.Settlement],
            ),
            BidAskOutlierConfigDto(
                model=OutlierAbsoluteBoundConfigDto(upperBound=10.0, lowerBound=-10.0),
                fieldsToBeValidated=[BidAskDataQualityField.LastPrice],
            ),
        ]
        for sample in samples:
            with self.subTest(type=type(sample).__name__):
                payload = artesianJsonSerialize(sample)

                self.assertEqual(payload["MarketDataType"], sample.marketDataType.name)
                self.assertEqual(artesianJsonDeserialize(payload, DataQualityRuleConfigDto), sample)

    def test_rule_config_serializes_discriminators(self: TestPolymorphicSerialization) -> None:
        payload = artesianJsonSerialize(
            OutlierConfigDto(model=OutlierRefCurveConfigDto(referenceMarketDataId=7, tolerancePerc=5.0))
        )

        self.assertEqual(payload["Type"], "Outlier")
        self.assertEqual(payload["Model"]["Type"], "Outlier")
        self.assertEqual(payload["Model"]["Model"], "RefCurve")

    def test_rule_config_without_details_falls_back_to_base(self: TestPolymorphicSerialization) -> None:
        for payload in ({"Type": "Outlier"}, {"Type": "CompletenessAndFreshness"}):
            with self.subTest(payload=payload):
                result = artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

                self.assertIs(type(result), DataQualityRuleConfigDto)

    def test_rule_config_rejects_unknown_discriminators(self: TestPolymorphicSerialization) -> None:
        payloads = (
            {"Type": "Outlier", "Model": {"Type": "Outlier", "Model": "Nope"}},
            {"Type": "Outlier", "Model": {"Type": "CompletenessAndFreshness", "Model": "RefCurve"}},
            {"Type": "Outlier", "MarketDataType": "Auction", "Model": {"Model": "AbsoluteBound"}},
            {"Type": "Nope", "MarketDataType": "ActualTimeSerie"},
            {"MarketDataType": "ActualTimeSerie"},
        )
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

    def test_outlier_model_decodes_to_concrete_types(self: TestPolymorphicSerialization) -> None:
        for model in (
            OutlierAbsoluteBoundConfigDto(upperBound=1.5, lowerBound=-1.5),
            OutlierRefCurveConfigDto(referenceMarketDataId=3, tolerancePerc=0.5),
        ):
            with self.subTest(type(model).__name__):
                result = artesianJsonDeserialize(artesianJsonSerialize(model), OutlierModelConfigDto)

                self.assertEqual(result, model)

    def test_outlier_model_type_is_optional_but_must_not_conflict(self: TestPolymorphicSerialization) -> None:
        result = artesianJsonDeserialize(
            {"Model": "RefCurve", "ReferenceMarketDataId": 3, "TolerancePerc": 0.5}, OutlierModelConfigDto
        )

        self.assertEqual(result, OutlierRefCurveConfigDto(referenceMarketDataId=3, tolerancePerc=0.5))
        with self.assertRaises(ValueError):
            artesianJsonDeserialize({"Type": "CompletenessAndFreshness", "Model": "RefCurve"}, OutlierModelConfigDto)

    def test_trigger_config_round_trips_to_concrete_types(self: TestPolymorphicSerialization) -> None:
        samples: list[TriggerConfigDto] = [
            OnEventTriggerConfigDto(),
            ScheduleTriggerConfigDto(CronScheduleDefinitionDto(cronExpression="0 8 * * *", timeZone="UTC")),
        ]
        for sample in samples:
            with self.subTest(type(sample).__name__):
                payload = artesianJsonSerialize(sample)

                self.assertEqual(payload["Type"], sample.type.name)
                self.assertEqual(artesianJsonDeserialize(payload, TriggerConfigDto), sample)

    def test_trigger_config_rejects_unknown_type(self: TestPolymorphicSerialization) -> None:
        with self.assertRaises(ValueError):
            artesianJsonDeserialize({"Type": "Nope"}, TriggerConfigDto)

    def test_schedule_definition_round_trips_and_rejects_unknown_type(self: TestPolymorphicSerialization) -> None:
        sample = CronScheduleDefinitionDto(cronExpression="0 8 * * *", timeZone="UTC")

        payload = artesianJsonSerialize(sample)

        self.assertEqual(payload["Type"], "Cron")
        self.assertEqual(artesianJsonDeserialize(payload, ScheduleDefinitionDto), sample)
        with self.assertRaises(ValueError):
            artesianJsonDeserialize({"Type": "Nope"}, ScheduleDefinitionDto)

    def test_polymorphic_value_decodes_through_json_bytes(self: TestPolymorphicSerialization) -> None:
        sample = QualityNotificationAlertDtoOutput(
            name="digest",
            triggerConfig=ScheduleTriggerConfigDto(
                CronScheduleDefinitionDto(cronExpression="0 8 * * *", timeZone="UTC")
            ),
            version=2,
        )

        result = artesianJsonDecode(artesianJsonEncode(sample), QualityNotificationAlertDtoOutput)

        self.assertEqual(result, sample)


class TestServiceWirePayloads(unittest.TestCase):
    """Hand-written payloads in the shape returned by the service."""

    def test_mas_outlier_payload(self: TestServiceWirePayloads) -> None:
        payload = {
            "Type": "Outlier",
            "MarketDataType": "MarketAssessment",
            "Model": {"Type": "Outlier", "Model": "AbsoluteBound", "UpperBound": 10.0, "LowerBound": -10.0},
            "Products": ["D+1"],
            "FieldsToBeValidated": ["Settlement"],
        }

        result = artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

        self.assertIs(type(result), MasOutlierConfigDto)
        result = cast(MasOutlierConfigDto, result)
        self.assertEqual(result.products, ["D+1"])
        self.assertEqual(result.fieldsToBeValidated, [MasDataQualityField.Settlement])
        self.assertEqual(result.model, OutlierAbsoluteBoundConfigDto(upperBound=10.0, lowerBound=-10.0))

    def test_bidask_outlier_payload(self: TestServiceWirePayloads) -> None:
        payload = {
            "Type": "Outlier",
            "MarketDataType": "BidAsk",
            "Model": {"Type": "Outlier", "Model": "AbsoluteBound", "UpperBound": 10.0, "LowerBound": -10.0},
            "Products": ["D+1"],
            "FieldsToBeValidated": ["LastPrice"],
        }

        result = artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

        self.assertIs(type(result), BidAskOutlierConfigDto)
        result = cast(BidAskOutlierConfigDto, result)
        self.assertEqual(result.products, ["D+1"])
        self.assertEqual(result.fieldsToBeValidated, [BidAskDataQualityField.LastPrice])

    def test_versioned_outlier_payload_decodes_to_outlier_config(self: TestServiceWirePayloads) -> None:
        payload = {
            "Type": "Outlier",
            "MarketDataType": "VersionedTimeSerie",
            "Model": {"Type": "Outlier", "Model": "RefCurve", "ReferenceMarketDataId": 7, "TolerancePerc": 5.0},
        }

        result = artesianJsonDeserialize(payload, DataQualityRuleConfigDto)

        self.assertIs(type(result), OutlierConfigDto)
        self.assertEqual(result.marketDataType, MarketDataType.VersionedTimeSerie)
        self.assertEqual(cast(OutlierConfigDto, result).model, OutlierRefCurveConfigDto(7, 5.0))

    def test_alert_schedule_events_payload(self: TestServiceWirePayloads) -> None:
        payload = {
            "ScheduleTime": "2024-05-01T08:00:00Z",
            "Events": {
                "Page": 1,
                "PageSize": 100,
                "Count": 1,
                "IsCountPartial": False,
                "Data": [
                    {
                        "MarketDataId": 10,
                        "RuleId": 2,
                        "AssignmentId": 3,
                        "Version": None,
                        "Product": "D+1",
                        "RangeImpacted": {"Start": "2024-05-01T00:00:00", "End": "2024-05-02T00:00:00"},
                        "NewStatus": "KO",
                        "OldStatus": "OK",
                        "Timestamp": "2024-05-01T07:59:00Z",
                        "RuleName": "rule",
                        "RuleVersion": 4,
                        "MarketDataName": "curve",
                        "Provider": "provider",
                    }
                ],
            },
        }

        result = artesianJsonDeserialize(payload, AlertScheduleEventsDtoOutput)

        self.assertIsInstance(result.events, PagedResultDqCheckChangeEventDtoOutput)
        self.assertEqual((result.events.page, result.events.pageSize, result.events.count), (1, 100, 1))
        self.assertFalse(result.events.isCountPartial)
        self.assertEqual(len(result.events.data), 1)
        event = result.events.data[0]
        self.assertIsInstance(event, DqCheckChangeEventDtoOutput)
        self.assertEqual((event.marketDataId, event.ruleId, event.assignmentId), (10, 2, 3))
        self.assertEqual(event.product, "D+1")
        self.assertEqual((event.newStatus, event.oldStatus), (CheckAggregatedStatus.KO, CheckAggregatedStatus.OK))
        self.assertEqual(event.rangeImpacted, LocalDateTimeRange(datetime(2024, 5, 1), datetime(2024, 5, 2)))
        self.assertEqual(event.ruleVersion, 4)


if __name__ == "__main__":
    unittest.main()
