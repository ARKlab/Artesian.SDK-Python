from __future__ import annotations
from Artesian import ArtesianConfig
from Artesian.Query import QueryService
from Artesian.MarketData import Granularity
from Artesian.MarketData import AggregationRule
from . import helpers
import unittest

from tests.helpers import Qs

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestVersioned(unittest.TestCase):
    @helpers.TrackRequests
    def test_Null_Fill(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forFilterId(1003)
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillNull()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "Null")

    @helpers.TrackRequests
    def test_No_Fill(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forFilterId(1003)
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillNone()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "NoFill")

    @helpers.TrackRequests
    def test_Latest_Fill(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forFilterId(1003)
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillLatestValue("P5D")
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "LatestValidValue")
        self.assertEqual(query["fillerP"], "P5D")
        self.assertEqual(query["fillerC"], "False")
        self.assertEqual(query["filterId"], "1003")

    @helpers.TrackRequests
    def test_Latest_Fill_Continue(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forFilterId(1003)
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillLatestValue("P5D", True)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "LatestValidValue")
        self.assertEqual(query["fillerP"], "P5D")
        self.assertEqual(query["fillerC"], "True")

    @helpers.TrackRequests
    def test_Custom_Value_Fill(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forFilterId(1003)
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillCustomValue(10)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "CustomValue")
        self.assertEqual(query["fillerDV"], "10")

    @helpers.TrackRequests
    def test_ForMostRecent(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .forMostRecent("2018-01-01", "2018-01-02")
            .withFillCustomValue(10)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerDV"], "10")

    @helpers.TrackRequests
    def test_ForMUVDateTime(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMUV()
            .withFillCustomValue(10)
            .execute()
        )

        path = requests.getPath()
        self.assertEqual(path, "/vts/Muv/Day/2021-09-22/2021-09-23")

    @helpers.TrackRequests
    def test_ForMUVVerionLimit(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMUV("2021-09-22T10:00:00")
            .withFillCustomValue(10)
            .execute()
        )

        path = requests.getPath()
        query = requests.getQs()
        self.assertEqual(query["versionLimit"], "2021-09-22T10:00:00")
        self.assertEqual(path, "/vts/Muv/Day/2021-09-22/2021-09-23")

    @helpers.TrackRequests
    def test_ForMostRecentDateTime(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMostRecent("2021-09-22T12:30:05", "2021-09-23T00:00:00")
            .withFillCustomValue(10)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerDV"], "10")

    @helpers.TrackRequests
    def test_ForMostRecentDateTimeFillNull(self: TestVersioned, requests: Qs) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMostRecent("2021-09-22T12:30:05", "2021-09-23T00:00:00")
            .withFillNull()
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "Null")

    @helpers.TrackRequests
    def test_UnitOfMeasure(self, requests):
        url = (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMostRecent("2021-09-22T12:30:05", "2021-09-23T00:00:00")
            .inUnitOfMeasure("kW")
            .withFillNull()
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["unitOfMeasure"], "kW")

    @helpers.TrackRequests
    def test_AggregationRule(self, requests):
        url = (
            qs.createVersioned()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forMostRecent("2021-09-22T12:30:05", "2021-09-23T00:00:00")
            .withAggregationRule(AggregationRule.AverageAndReplicate)
            .withFillNull()
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["aggregationRule"], "AggregationRule.AverageAndReplicate")
