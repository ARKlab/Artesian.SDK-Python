from dataclasses import asdict
from Artesian import *
import responses
import unittest
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize

cfg = ArtesianConfig("https://baseurl.com","apikey")


class TestMarketDataService(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__service = MarketDataService(cfg)
        self.__sampleOutput = MarketDataEntityOutput(
            providerName = "PROVIDER",
            marketDataName = "MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataType.ActualTimeSerie,
            originalTimezone="CET"
        )
        self.__serializedOutput = artesianJsonSerialize(self.__sampleOutput)
        self.__sampleInput = artesianJsonSerialize(MarketDataEntityInput(
            providerName = "PROVIDER",
            marketDataName = "MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataType.ActualTimeSerie,
            originalTimezone="CET"
        ))
        self.maxDiff = None
        self.__baseurl = 'https://baseurl.com/v2.1'
        return super().setUp()

    async def test_registerMarketData(self):
        with responses.RequestsMock() as rsps:
            rsps.add('POST', self.__baseurl + '/marketdata/entity', json=self.__serializedOutput, status=200)

            output = await self.__service.registerMarketDataAsync(self.__sampleInput)

            self.assertEqual(asdict(output), asdict(self.__sampleOutput))
