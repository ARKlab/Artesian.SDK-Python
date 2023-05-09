from Artesian import ArtesianConfig
from Artesian.MarketData import Granularity
from Artesian.Query import QueryService
from . import helpers
import unittest

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestActual(unittest.TestCase):
    @helpers.TrackRequests
    def test_Null_Fill(self, requests):
        url = (
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
    def test_No_Fill(self, requests):
        url = (
            qs.createActual()
            .forFilterId(1003)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inTimeZone("UTC")
            .inGranularity(Granularity.Hour)
            .withFillNone()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "NoFill")

    @helpers.TrackRequests
    def test_Latest_Fill(self, requests):
        url = (
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
    def test_Latest_Fill_Continue(self, requests):
        url = (
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
    def test_Custom_Value_Fill(self, requests):
        url = (
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
