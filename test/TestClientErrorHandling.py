from Artesian import *
from Artesian._ClientsExecutor.Client import _Client
import helpers
import unittest
import responses
import requests

class TestClientErrorHandling(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self._client = _Client("https://httpbin.org","apikey")

    @responses.activate
    async def test_on404returnNone(self):
        responses.add('GET', 'https://httpbin.org/status/401', body='', status=404)

        with self._client as c:
            res = await c.exec('GET', "/status/401")

        self.assertIsNone(res, "Response should be None on 404")
    
    @responses.activate  
    async def testExample(self):
        responses.add(**{
            'method'         : responses.GET,
            'url'            : 'http://example.com/api/123',
            'body'           : '{"error": "reason"}',
            'status'         : 404,
            'content_type'   : 'application/json',
            'adding_headers' : {'X-Foo': 'Bar'}
        })

        response = requests.get('http://example.com/api/123')

        self.assertEqual({'error': 'reason'}, response.json())
        self.assertEqual(404, response.status_code)