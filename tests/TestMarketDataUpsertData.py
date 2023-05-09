from Artesian import ArtesianConfig
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from Artesian.MarketData import (
    MarketDataService,
    MarketDataIdentifier,
    UpsertData,
    MarketAssessmentValue,
    BidAskValue,
    AuctionBids,
    AuctionBidValue,
)
from datetime import datetime
import responses
import unittest

from dateutil import tz

cfg = ArtesianConfig("https://baseurl.com", "APIKey")


class TestMarketDataServiceUpsertData(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__service = MarketDataService(cfg)
        self.maxDiff = None
        self.__baseurl = "https://baseurl.com/v2.1"

        return super().setUp()

    async def test_upsertDateSerie(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Timezone": "CET",
            "Rows": [
                {"Key": "2020-01-01T01:00:00.000000", "Value": 42.0},
                {"Key": "2020-01-02T02:00:00.000000", "Value": 43.0},
            ],
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
            "KeepNulls": False,
            "DownloadedAt": "2020-01-03T00:00:00.000000Z",
        }
        upsert = UpsertData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            rows={
                datetime(2020, 1, 1, 1): 42.0,
                datetime(2020, 1, 2, 2): 43.0,
            },
            downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
        )
        ser = artesianJsonSerialize(upsert)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/upsertdata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.upsertDataAsync(upsert)

            self.assertEqual(len(rsps.calls), 1)

    async def test_upsertDateSerieMA(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "MarketAssessment": [
                {
                    "Key": "2020-01-01T00:00:00.000000",
                    "Value": [
                        {"Key": "Feb-20", "Value": {"Open": 10.0, "Close": 11.0}},
                        {"Key": "Mar-20", "Value": {"Open": 20.0, "Close": 21.0}},
                    ],
                },
                {
                    "Key": "2020-01-02T00:00:00.000000",
                    "Value": [
                        {
                            "Key": "Feb-20",
                            "Value": {"Open": 11.0, "Close": 12.0},
                        },
                        {"Key": "Mar-20", "Value": {"Open": 21.0, "Close": 22.0}},
                    ],
                },
            ],
            "Timezone": "CET",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
            "KeepNulls": False,
            "DownloadedAt": "2020-01-03T00:00:00.000000Z",
        }
        upsert = UpsertData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            marketAssessment={
                datetime(2020, 1, 1): {
                    "Feb-20": MarketAssessmentValue(open=10.0, close=11.0),
                    "Mar-20": MarketAssessmentValue(open=20.0, close=21.0),
                },
                datetime(2020, 1, 2): {
                    "Feb-20": MarketAssessmentValue(open=11.0, close=12.0),
                    "Mar-20": MarketAssessmentValue(open=21.0, close=22.0),
                },
            },
            downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
        )
        ser = artesianJsonSerialize(upsert)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/upsertdata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.upsertDataAsync(upsert)

            self.assertEqual(len(rsps.calls), 1)

    async def test_upsertDateSerieBA(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "BidAsk": [
                {
                    "Key": "2020-01-01T00:00:00.000000",
                    "Value": [
                        {
                            "Key": "Feb-20",
                            "Value": {"BestBidPrice": 15.0, "LastQuantity": 14.0},
                        },
                        {
                            "Key": "Mar-20",
                            "Value": {"BestBidPrice": 25.0, "LastQuantity": 24.0},
                        },
                    ],
                },
                {
                    "Key": "2020-01-02T00:00:00.000000",
                    "Value": [
                        {
                            "Key": "Feb-20",
                            "Value": {"BestBidPrice": 15.0, "LastQuantity": 14.0},
                        },
                        {
                            "Key": "Mar-20",
                            "Value": {"BestBidPrice": 25.0, "LastQuantity": 24.0},
                        },
                    ],
                },
            ],
            "Timezone": "CET",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
            "KeepNulls": False,
            "DownloadedAt": "2020-01-03T00:00:00.000000Z",
        }
        upsert = UpsertData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            bidAsk={
                datetime(2020, 1, 1): {
                    "Feb-20": BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
                    "Mar-20": BidAskValue(bestBidPrice=25.0, lastQuantity=24.0),
                },
                datetime(2020, 1, 2): {
                    "Feb-20": BidAskValue(bestBidPrice=15.0, lastQuantity=14.0),
                    "Mar-20": BidAskValue(bestBidPrice=25.0, lastQuantity=24.0),
                },
            },
            downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
        )
        ser = artesianJsonSerialize(upsert)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/upsertdata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.upsertDataAsync(upsert)

            self.assertEqual(len(rsps.calls), 1)

    async def test_upsertDateSerieAU(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "AuctionRows": [
                {
                    "Key": "2020-01-01T00:00:00.000000",
                    "Value": {
                        "BidTimestamp": "2020-01-01T00:00:00.000000",
                        "Bid": [
                            {"Price": 11.0, "Quantity": 12.0},
                            {"Price": 13.0, "Quantity": 14.0},
                        ],
                        "Offer": [
                            {"Price": 21.0, "Quantity": 22.0},
                            {"Price": 23.0, "Quantity": 24.0},
                        ],
                    },
                }
            ],
            "Timezone": "CET",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
            "KeepNulls": False,
            "DownloadedAt": "2020-01-03T00:00:00.000000Z",
        }
        upsert = UpsertData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            auctionRows={
                datetime(2020, 1, 1): AuctionBids(
                    datetime(2020, 1, 1),
                    bid=[
                        AuctionBidValue(11.0, 12.0),
                        AuctionBidValue(13.0, 14.0),
                    ],
                    offer=[
                        AuctionBidValue(21.0, 22.0),
                        AuctionBidValue(23.0, 24.0),
                    ],
                )
            },
            downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
        )
        ser = artesianJsonSerialize(upsert)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/upsertdata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.upsertDataAsync(upsert)

            self.assertEqual(len(rsps.calls), 1)
