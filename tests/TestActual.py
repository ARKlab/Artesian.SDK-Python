from Artesian import ArtesianConfig
from Artesian.MarketData import Granularity
from Artesian.MarketData import CommonUnitOfMeasure
from Artesian.Query import (
    ActualQuery,
    AuctionQuery,
    BidAskQuery,
    MasQuery,
    QueryService,
    VersionedQuery,
)
from Artesian.Query._Query import _Query
from Artesian.MarketData import AggregationRule
from . import helpers
from tests.helpers import Qs
import unittest
from typing import get_type_hints

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestActual(unittest.TestCase):
    def test_execution_return_type_contracts(self) -> None:
        for query_type, method in (
            (ActualQuery, "execute"),
            (AuctionQuery, "execute"),
            (BidAskQuery, "execute"),
            (MasQuery, "execute"),
            (VersionedQuery, "execute"),
            (_Query, "_exec"),
        ):
            for name in (method, method + "Async"):
                with self.subTest(query=query_type.__name__, method=name):
                    self.assertEqual(
                        get_type_hints(getattr(query_type, name))["return"],
                        list[object],
                    )

    @helpers.TrackRequests
    def test_Null_Fill(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillNull()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "Null")

    @helpers.TrackRequests
    def test_No_Fill(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillNone()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "NoFill")
        self.assertEqual(requests.getQs()["filterId"], "1003")

    @helpers.TrackRequests
    def test_Latest_Fill(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
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

    @helpers.TrackRequests
    def test_Latest_Fill_Continue(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
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
    def test_Custom_Value_Fill(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
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
    def test_UnitOfMeasure(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .inUnitOfMeasure(CommonUnitOfMeasure.kW)
            .withFillCustomValue(10)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["unitOfMeasure"], CommonUnitOfMeasure.kW)

    @helpers.TrackRequests
    def test_AggregationRule(self, requests: Qs) -> None:
        (
            qs.createActual()
            .forFilterId(1003)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withAggregationRule(AggregationRule.AverageAndReplicate)
            .withFillCustomValue(10)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["aggregationRule"], "AggregationRule.AverageAndReplicate")
