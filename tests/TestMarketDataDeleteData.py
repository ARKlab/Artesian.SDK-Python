from Artesian import ArtesianConfig
from Artesian.MarketData._Dto.UpsertData import BidAskValue
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from Artesian.MarketData import (
    MarketDataService,
    MarketDataIdentifier,
    DeleteData
)
from datetime import datetime
import responses
import unittest

from dateutil import tz

cfg = ArtesianConfig("https://baseurl.com", "APIKey")


class TestMarketDataServiceDeleteData(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__service = MarketDataService(cfg)
        self.maxDiff = None
        self.__baseurl = "https://baseurl.com/v2.1"

        return super().setUp()

    async def test_deleteDateSerie(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Timezone": "CET",
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            rangeStart=datetime(2020, 1, 1, 1),
            rangeEnd=datetime(2020, 1, 3, 1),
        )
        ser = artesianJsonSerialize(delete)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/deletedata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.deleteDataAsync(delete)

            self.assertEqual(len(rsps.calls), 1)

    async def test_deleteDateSerieMA(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Timezone": "CET",
            "Product": ["Jan-15"],
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            product=["Jan-15"],
            rangeStart=datetime(2020, 1, 1, 1),
            rangeEnd=datetime(2020, 1, 3, 1),
        )
        ser = artesianJsonSerialize(delete)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/deletedata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.deleteDataAsync(delete)

            self.assertEqual(len(rsps.calls), 1)

    async def test_deleteVersionedSerie(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Timezone": "CET",
            "Version": "2020-01-01T01:00:00.000000",
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            "CET",
            rangeStart=datetime(2020, 1, 1, 1),
            rangeEnd=datetime(2020, 1, 3, 1),
            version=datetime(2020, 1, 1, 1)
        )
        ser = artesianJsonSerialize(delete)
        self.assertEqual(ser, expectedJson)

        with responses.RequestsMock() as rsps:
            rsps.add(
                "POST",
                self.__baseurl + "/marketdata/deletedata",
                match=[responses.matchers.json_params_matcher(expectedJson)],
                status=200,
            )

            await self.__service.deleteDataAsync(delete)

            self.assertEqual(len(rsps.calls), 1)


    # async def test_deleteDateSerieBA(self):
    #     expectedJson = {
    #         "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
    #         "BidAsk": [
    #             {
    #                 "Key": "2020-01-01T00:00:00.000000",
    #                 "Value": [
    #                     {
    #                         "Key": "Feb-20",
    #                         "Value": {"BestBidPrice": 15.0, "LastQuantity": 14.0},
    #                     },
    #                     {
    #                         "Key": "Mar-20",
    #                         "Value": {"BestBidPrice": 25.0, "LastQuantity": 24.0},
    #                     },
    #                 ],
    #             },
    #             {
    #                 "Key": "2020-01-02T00:00:00.000000",
    #                 "Value": [
    #                     {
    #                         "Key": "Feb-20",
    #                         "Value": {"BestBidPrice": 15.0, "LastQuantity": 14.0},
    #                     },
    #                     {
    #                         "Key": "Mar-20",
    #                         "Value": {"BestBidPrice": 25.0, "LastQuantity": 24.0},
    #                     },
    #                 ],
    #             },
    #         ],
    #         "Timezone": "CET",
    #         "DeferCommandExecution": False,
    #         "DeferDataGeneration": True,
    #         "KeepNulls": False,
    #         "DownloadedAt": "2020-01-03T00:00:00.000000Z",
    #     }
    #     delete = DeleteData(
    #         MarketDataIdentifier("PROVIDER", "CURVENAME"),
    #         "CET",
    #         product=
    #         [ "Feb-20","Mar-20"
    #             # { "Key": "2020-01-01T00:00:00.000000", "Value" : [ 
    #             #     { "Key": "Feb-20", "Value": { "BestBidPrice": 15.0, "LastQuantity": 14.0 } },
    #             #     { "key": "Mar-20", "Value": { "BestBidPrice": 25.0, "LastQuantity": 24.0 } } ] 
    #             # },
    #             # { "Key": "2020-01-02T00:00:00.000000", "Value": [ 
    #             #     { "Key": "Feb-20", "Value": { "BestBidPrice": 15.0, "LastQuantity": 14.0 } },
    #             #     { "Key": "Mar-20", "Value": { "BestBidPrice": 25.0, "LastQuantity": 24.0 } } ] 
    #             # }
    #         ],
    #         rangeStart=datetime(2020, 1, 1, 0),
    #         rangeEnd=datetime(2020, 1, 2, 1),
    #     )
    #     ser = artesianJsonSerialize(delete)
    #     self.assertEqual(ser, expectedJson)

    #     with responses.RequestsMock() as rsps:
    #         rsps.add(
    #             "POST",
    #             self.__baseurl + "/marketdata/deletedata",
    #             match=[responses.matchers.json_params_matcher(expectedJson)],
    #             status=200,
    #         )

    #         await self.__service.deleteDataAsync(delete)

    #         self.assertEqual(len(rsps.calls), 1)

    # async def test_upsertDateSerieAU(self):
    #     expectedJson = {
    #         "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
    #         "AuctionRows": [
    #             {
    #                 "Key": "2020-01-01T00:00:00.000000",
    #                 "Value": {
    #                     "BidTimestamp": "2020-01-01T00:00:00.000000",
    #                     "Bid": [
    #                         {"Price": 11.0, "Quantity": 12.0},
    #                         {"Price": 13.0, "Quantity": 14.0},
    #                     ],
    #                     "Offer": [
    #                         {"Price": 21.0, "Quantity": 22.0},
    #                         {"Price": 23.0, "Quantity": 24.0},
    #                     ],
    #                 },
    #             }
    #         ],
    #         "Timezone": "CET",
    #         "DeferCommandExecution": False,
    #         "DeferDataGeneration": True,
    #         "KeepNulls": False,
    #         "DownloadedAt": "2020-01-03T00:00:00.000000Z",
    #     }
    #     upsert = UpsertData(
    #         MarketDataIdentifier("PROVIDER", "CURVENAME"),
    #         "CET",
    #         auctionRows={
    #             datetime(2020, 1, 1): AuctionBids(
    #                 datetime(2020, 1, 1),
    #                 bid=[
    #                     AuctionBidValue(11.0, 12.0),
    #                     AuctionBidValue(13.0, 14.0),
    #                 ],
    #                 offer=[
    #                     AuctionBidValue(21.0, 22.0),
    #                     AuctionBidValue(23.0, 24.0),
    #                 ],
    #             )
    #         },
    #         downloadedAt=datetime(2020, 1, 3).replace(tzinfo=tz.UTC),
    #     )
    #     ser = artesianJsonSerialize(upsert)
    #     self.assertEqual(ser, expectedJson)

    #     with responses.RequestsMock() as rsps:
    #         rsps.add(
    #             "POST",
    #             self.__baseurl + "/marketdata/upsertdata",
    #             match=[responses.matchers.json_params_matcher(expectedJson)],
    #             status=200,
    #         )

    #         await self.__service.upsertDataAsync(upsert)

    #         self.assertEqual(len(rsps.calls), 1)