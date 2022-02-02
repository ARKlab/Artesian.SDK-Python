from Artesian import *
from Artesian._ClientsExecutor.Client import _Client
import helpers
import unittest
import responses
import requests

class TestClientErrorHandling(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self._client = _Client("https://baseurl.com","apikey")

    #@responses.activate cannot be used with responses<0.19 with 'async' methods
    async def test_on404returnNone(self):
        with responses.RequestsMock() as rsps:
            rsps.add('GET', 'https://baseurl.com/404', body='', status=404)

            with self._client as c:
                res = await c.exec('GET', "/404")

            self.assertIsNone(res, "Response should be None on 404")

    async def test_success(self):
        with responses.RequestsMock() as rsps:
            rsps.add('GET', 'https://baseurl.com/200', body='{"result":true}', status=200, content_type='application/json')

            with self._client as c:
                res = await c.exec('GET', "/200")

            self.assertEqual(res, {'result': True})

    async def test_problemDetails(self):
        cases = [
            (400, ArtesianSdkValidationException), 
            (409, ArtesianSdkOptimisticConcurrencyException),
            (412, ArtesianSdkOptimisticConcurrencyException),
            (401, ArtesianSdkForbiddenException),
            (403, ArtesianSdkForbiddenException),
            (500, ArtesianSdkRemoteException)
            ]
        for code, excls in cases:
            with self.subTest(str(code) + "=>" + excls.__name__):
                with responses.RequestsMock() as rsps:
                    problemDetails = {'type': "TYPE", 'title':"TITLE", 'details':"DETAILS", 'other': { 'more': "data" } }
                    rsps.add('GET', 'https://baseurl.com/'+str(code), json=problemDetails, status=code, content_type='application/problem+json')

                    with self.assertRaises(excls) as ex:
                        with self._client as c:
                            res = await c.exec('GET', "/"+str(code))
                    
                    self.assertEqual(ex.exception.statusCode, code)
                    self.assertIsNone(ex.exception.errorText)
                    self.assertEqual(ex.exception.problemDetails, problemDetails)
                    self.assertEqual(ex.exception.message, "Failed REST call to Artesian. GET https://baseurl.com/{} returned {}. DETAILS".format(code,code))

    
    async def test_problemDetailsWithoutDetails(self):
        with responses.RequestsMock() as rsps:
            problemDetails = {'type': "TYPE", 'title':"TITLE", 'other': { 'more': "data" } }
            rsps.add('GET', 'https://baseurl.com/'+str(400), json=problemDetails, status=400, content_type='application/problem+json')

            with self.assertRaises(ArtesianSdkValidationException) as ex:
                with self._client as c:
                    res = await c.exec('GET', "/"+str(400))
            
            self.assertEqual(ex.exception.statusCode, 400)
            self.assertIsNone(ex.exception.errorText)
            self.assertEqual(ex.exception.problemDetails, problemDetails)
            self.assertEqual(ex.exception.message, "Failed REST call to Artesian. GET https://baseurl.com/400 returned 400. TITLE")


    async def test_NOT_problemDetails(self):
        cases = [
            (400, ArtesianSdkValidationException), 
            (409, ArtesianSdkOptimisticConcurrencyException),
            (412, ArtesianSdkOptimisticConcurrencyException),
            (401, ArtesianSdkForbiddenException),
            (403, ArtesianSdkForbiddenException),
            (500, ArtesianSdkRemoteException)
            ]
        for code, excls in cases:
            with self.subTest(str(code) + "=>" + excls.__name__):
                with responses.RequestsMock() as rsps:
                    body = "BODY STRING"
                    rsps.add('GET', 'https://baseurl.com/'+str(code), body=body, status=code, content_type='text/plain')

                    with self.assertRaises(excls) as ex:
                        with self._client as c:
                            res = await c.exec('GET', "/"+str(code))
                    
                    self.assertEqual(ex.exception.statusCode, code)
                    self.assertIsNone(ex.exception.problemDetails)
                    self.assertEqual(ex.exception.errorText, body)
                    self.assertEqual(ex.exception.message, "Failed REST call to Artesian. GET https://baseurl.com/{} returned {}. BODY STRING".format(code,code))

    
        