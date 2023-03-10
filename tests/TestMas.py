from Artesian import ArtesianConfig
from Artesian.Query import QueryService
from . import helpers
import unittest

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestMas(unittest.TestCase):
    @helpers.TrackRequests
    def test_Null_Fill(self, requests):
        url = (
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withFillNull()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "Null")

    @helpers.TrackRequests
    def test_No_Fill(self, requests):
        url = (
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withFillNone()
            .execute()
        )

        self.assertEqual(requests.getQs()["fillerK"], "NoFill")

    @helpers.TrackRequests
    def test_Latest_Fill(self, requests):
        url = (
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
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
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withFillLatestValue("P5D", "True")
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "LatestValidValue")
        self.assertEqual(query["fillerP"], "P5D")
        self.assertEqual(query["fillerC"], "True")

    @helpers.TrackRequests
    def test_Custom_Value_Fill(self, requests):
        url = (
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withFillCustomValue(
                settlement=1,
                open=2,
                close=3,
                high=4,
                low=5,
                volumePaid=6,
                volumeGiven=7,
                volume=8,
            )
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "CustomValue")
        self.assertEqual(query["fillerDVs"], "1")
        self.assertEqual(query["fillerDVo"], "2")
        self.assertEqual(query["fillerDVc"], "3")
        self.assertEqual(query["fillerDVh"], "4")
        self.assertEqual(query["fillerDVl"], "5")
        self.assertEqual(query["fillerDVvp"], "6")
        self.assertEqual(query["fillerDVvg"], "7")
        self.assertEqual(query["fillerDVvt"], "8")
