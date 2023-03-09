from Artesian import ArtesianConfig
from Artesian.Query import QueryService
from . import helpers
import unittest

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestBidAsk(unittest.TestCase):
    @helpers.TrackRequests
    def test_Null_Fill(self, requests):
        url = (
            qs.createBidAsk()
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
            qs.createBidAsk()
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
            qs.createBidAsk()
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
            qs.createBidAsk()
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
            qs.createBidAsk()
            .forMarketData([100000001])
            .forProducts(["M+1", "M+2"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withFillCustomValue(
                bestBidPrice=1,
                bestAskPrice=2,
                bestBidQuantity=3,
                bestAskQuantity=4,
                lastPrice=5,
                lastQuantity=6,
            )
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["fillerK"], "CustomValue")
        self.assertEqual(query["fillerDVbbp"], "1")
        self.assertEqual(query["fillerDVbap"], "2")
        self.assertEqual(query["fillerDVbbq"], "3")
        self.assertEqual(query["fillerDVbaq"], "4")
        self.assertEqual(query["fillerDVlp"], "5")
        self.assertEqual(query["fillerDVlq"], "6")
