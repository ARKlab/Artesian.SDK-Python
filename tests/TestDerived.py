from __future__ import annotations
from Artesian import ArtesianConfig
from Artesian.Query import QueryService
from Artesian.MarketData import Granularity
from . import helpers
import unittest

from tests.helpers import Qs

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = QueryService(cfg)


class TestDerived(unittest.TestCase):
    @helpers.TrackRequests
    def test_ForDerivedDateTime(self: TestDerived, requests: Qs) -> None:
        (
            qs.createDerived()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2021-09-22", "2021-09-23")
            .inTimeZone("CET")
            .inGranularity(Granularity.Day)
            .forDerived()
            .withFillCustomValue(10)
            .execute()
        )

        path = requests.getPath()
        self.assertEqual(path, "/vts/Muv/Day/2021-09-22/2021-09-23")
