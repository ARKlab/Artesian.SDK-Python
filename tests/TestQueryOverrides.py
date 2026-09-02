import unittest

from Artesian import ArtesianConfig
from Artesian.MarketData import Granularity
from Artesian.Query import QueryService
from . import helpers
from .helpers import Qs


cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
qs = QueryService(cfg)


class TestQueryOverrides(unittest.TestCase):
    def assertOverrideParams(self: "TestQueryOverrides", requests: Qs) -> None:
        query = requests.getQs()
        self.assertEqual(query["includeOverrideDetails"], "true")
        self.assertEqual(query["skipOverrides"], "true")

    @helpers.TrackRequests
    def test_actual_override_options(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createActual()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inGranularity(Granularity.Hour)
            .withSkipOverrides()
            .withIncludeOverrideDetails()
            .execute()
        )

        self.assertOverrideParams(requests)

    @helpers.TrackRequests
    def test_versioned_override_options(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createVersioned()
            .forMarketData([100000001])
            .forLastNVersions(1)
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inGranularity(Granularity.Hour)
            .withSkipOverrides()
            .withIncludeOverrideDetails()
            .execute()
        )

        self.assertOverrideParams(requests)

    @helpers.TrackRequests
    def test_market_assessment_override_options(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createMarketAssessment()
            .forMarketData([100000001])
            .forProducts(["M+1"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withSkipOverrides()
            .withIncludeOverrideDetails()
            .execute()
        )

        self.assertOverrideParams(requests)

    @helpers.TrackRequests
    def test_auction_override_options(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createAuction()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withSkipOverrides()
            .withIncludeOverrideDetails()
            .execute()
        )

        self.assertOverrideParams(requests)

    @helpers.TrackRequests
    def test_bid_ask_override_options(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createBidAsk()
            .forMarketData([100000001])
            .forProducts(["M+1"])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .withSkipOverrides()
            .withIncludeOverrideDetails()
            .execute()
        )

        self.assertOverrideParams(requests)

    @helpers.TrackRequests
    def test_override_options_default_to_false(
        self: "TestQueryOverrides", requests: Qs
    ) -> None:
        (
            qs.createActual()
            .forMarketData([100000001])
            .inAbsoluteDateRange("2018-01-01", "2018-01-02")
            .inGranularity(Granularity.Hour)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["includeOverrideDetails"], "false")
        self.assertEqual(query["skipOverrides"], "false")


if __name__ == "__main__":
    unittest.main()
