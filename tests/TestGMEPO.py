from Artesian import ArtesianConfig
from Artesian.GMEPublicOffers import (
    GMEPublicOfferService,
    Market,
    Purpose,
    Status,
    Zone,
)
from . import helpers
import unittest
from urllib.parse import unquote
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
import responses

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")

qs = GMEPublicOfferService(cfg)


class TestGMEPO(unittest.TestCase):

    def setUp(self) -> None:
        self.__baseurl = "https://arkive.artesian.cloud/tenantName//"
        self.__sampleOutput = dict(
            Page=1,
            PageSize=10,
            Count=0,
            IsCountPartial=False,
            Data=[[]],
        )
        self.__serializedOutput = artesianJsonSerialize(self.__sampleOutput)

        return super().setUp()

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

        query = requests.getQs()
        self.assertEqual(query["market"], "MGP")

    @helpers.TrackGMEPORequests
    def test_Markets(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forMarket([Market.MGP, Market.MI1, Market.MIA2, Market.MIXBID])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["market"], "MGP,MI1,MIA2,MIXBID")

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

        query = requests.getQs()
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

        query = requests.getQs()
        self.assertEqual(query["zone"], "NORD,SUD")

    @helpers.TrackGMEPORequests
    def test_Operator(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forOperators(["Test"])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["operators"], "Test")

    @helpers.TrackGMEPORequests
    def test_Pagination(self, requests):
        url = (
            qs.createQuery()
            .forDate("2020-04-01")
            .forZone([Zone.NORD, Zone.SUD])
            .forStatus(Status.ACC)
            .forPurpose(Purpose.BID)
            .withPagination(1, 100)
            .execute()
        )

        query = requests.getQs()
        self.assertEqual(query["page"], "1")
        self.assertEqual(query["pageSize"], "100")

    def test_checkreturnedPayload(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                "GET",
                self.__baseurl
                + "gmepublicoffer/v2.0/extract/2024-01-21/BID/ACC?_=1&page=1&pageSize=10",
                json=self.__sampleOutput,
                status=200,
            )

            output = (
                qs.createQuery()
                .forDate("2024-01-21")
                .forStatus(Status.ACC)
                .forPurpose(Purpose.BID)
                .withPagination(1, 10)
                .execute()
            )

        self.assertEqual(output, self.__sampleOutput)
