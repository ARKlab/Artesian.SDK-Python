from datetime import date, datetime
import unittest

from Artesian._ClientsExecutor.ArtesianJsonSerializer import (
    artesianJsonDeserialize,
    artesianJsonSerialize,
)
from Artesian.MarketData import (
    ActualCompletenessAndFreshnessConfigDto,
    DataQualityStatusSummaryDto,
    OnEventTriggerConfigDto,
    OutlierAbsoluteBoundConfigDto,
    OutlierConfigDto,
    ScheduleTriggerConfigDto,
)
from Artesian.MarketData._Dto.CheckResultExtract import (
    CheckResultExtractTs,
    CheckResultExtractVts,
)
from Artesian.MarketData._Dto.DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoOutput,
)


class TestDataQualitySerialization(unittest.TestCase):
    def test_compact_extract_ts_round_trip(
        self: "TestDataQualitySerialization",
    ) -> None:
        payload = {
            "P": "provider",
            "C": "curve",
            "R": "rule",
            "AID": 3,
            "MKID": 4,
            "RID": 5,
            "T": "2024-01-01T00:00:00.000000",
            "D": 2,
            "S": "2024-01-01T00:00:00.000000",
            "E": "2024-01-02T00:00:00.000000",
        }

        result = artesianJsonDeserialize(payload, CheckResultExtractTs)

        self.assertEqual(result.assignmentId, 3)
        self.assertEqual(artesianJsonSerialize(result), payload)

    def test_compact_extract_vts_uses_version_key(
        self: "TestDataQualitySerialization",
    ) -> None:
        result = CheckResultExtractVts(
            time=datetime(2024, 1, 1),
            issueCount=2,
            competenceStart=datetime(2024, 1, 1),
            competenceEnd=datetime(2024, 1, 2),
            version=datetime(2023, 12, 31),
        )

        payload = artesianJsonSerialize(result)

        self.assertEqual(payload["V"], "2023-12-31T00:00:00.000000")
        self.assertNotIn("Version", payload)

    def test_rule_configuration_is_deserialized_to_concrete_types(
        self: "TestDataQualitySerialization",
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

        self.assertIsInstance(
            actual.configuration, ActualCompletenessAndFreshnessConfigDto
        )
        self.assertEqual(
            actual.configuration.scheduleConfig.scheduleDefinition.cronExpression,
            "0 0 * * *",
        )
        self.assertIsInstance(outlier.configuration, OutlierConfigDto)
        self.assertIsInstance(
            outlier.configuration.model, OutlierAbsoluteBoundConfigDto
        )

    def test_alert_trigger_is_deserialized_to_concrete_type(
        self: "TestDataQualitySerialization",
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

        scheduled = artesianJsonDeserialize(
            scheduledPayload, QualityNotificationAlertDtoOutput
        )
        onEvent = artesianJsonDeserialize(
            onEventPayload, QualityNotificationAlertDtoOutput
        )

        self.assertIsInstance(scheduled.triggerConfig, ScheduleTriggerConfigDto)
        self.assertIsInstance(onEvent.triggerConfig, OnEventTriggerConfigDto)

    def test_status_summary_maps_from_api_field(
        self: "TestDataQualitySerialization",
    ) -> None:
        payload = {"From": "2024-01-01", "To": "2024-01-02"}

        result = artesianJsonDeserialize(payload, DataQualityStatusSummaryDto)

        self.assertEqual(result.from_, date(2024, 1, 1))
        self.assertEqual(artesianJsonSerialize(result)["From"], "2024-01-01")


if __name__ == "__main__":
    unittest.main()
