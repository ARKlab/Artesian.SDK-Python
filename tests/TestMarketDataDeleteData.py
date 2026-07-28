from Artesian import ArtesianConfig
from Artesian.MarketData._Dto.UpsertData import BidAskValue
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from Artesian.MarketData import MarketDataService, MarketDataIdentifier, DeleteData
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
            timezone="CET",
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

    async def test_deleteDateSerieWithoutTimezone(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
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

    async def test_deleteDateSerieWithProduct(self):
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
            timezone="CET",
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

    async def test_deleteDateSerieWithProductWithoutTimezone(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Product": ["Jan-15"],
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
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
            timezone="CET",
            rangeStart=datetime(2020, 1, 1, 1),
            rangeEnd=datetime(2020, 1, 3, 1),
            version=datetime(2020, 1, 1, 1),
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

    async def test_deleteVersionedSerieWithoutTimezone(self):
        expectedJson = {
            "ID": {"Provider": "PROVIDER", "Name": "CURVENAME"},
            "Version": "2020-01-01T01:00:00.000000",
            "RangeStart": "2020-01-01T01:00:00.000000",
            "RangeEnd": "2020-01-03T01:00:00.000000",
            "DeferCommandExecution": False,
            "DeferDataGeneration": True,
        }
        delete = DeleteData(
            MarketDataIdentifier("PROVIDER", "CURVENAME"),
            rangeStart=datetime(2020, 1, 1, 1),
            rangeEnd=datetime(2020, 1, 3, 1),
            version=datetime(2020, 1, 1, 1),
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
