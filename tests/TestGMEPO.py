from Artesian import ArtesianConfig
from Artesian.GMEPublicOffers import (
    GMEPublicOfferService,
    Market,
    Purpose,
    Status,
    Zone
)
from . import helpers
import unittest

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = GMEPublicOfferService(cfg)


class TestGMEPO(unittest.TestCase):
    @helpers.TrackGMEPORequests
    def test_Market(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forMarket([Market.MGP])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getPOQs()
        self.assertEqual(query["market"], "MGP")

    @helpers.TrackGMEPORequests
    def test_Markets(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forMarket([Market.MGP,Market.MI1])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getPOQs()
        self.assertEqual(query["market"], "MGP,MI1")

    @helpers.TrackGMEPORequests
    def test_Zone(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forZone([Zone.NORD])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getPOQs()
        self.assertEqual(query["zone"], "NORD")

    @helpers.TrackGMEPORequests
    def test_Zones(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forZone([Zone.NORD, Zone.SUD])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getPOQs()
        self.assertEqual(query["zone"], "NORD,SUD")

    @helpers.TrackGMEPORequests
    def test_Pagination(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forZone([Zone.NORD, Zone.SUD])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .withPagination(1,100)
            .execute()
        )

        query = requests.getPOQs()
        self.assertEqual(query["page"], "1")
        self.assertEqual(query["pageSize"], "100")