from Artesian import ArtesianConfig
import responses
import unittest
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize
from Artesian.MarketData import *

cfg = ArtesianConfig("https://baseurl.com","apikey")

class TestMarketDataServiceMarketData(unittest.IsolatedAsyncioTestCase):
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
        self.__sampleInput = MarketDataEntityInput(
            providerName = "PROVIDER",
            marketDataName = "MARKETDATA",
            originalGranularity=Granularity.Day,
            type=MarketDataType.ActualTimeSerie,
            originalTimezone="CET",
            tags={
                'PythonTag': ['PythonTagValue1', 'PythonTagValue2']
            }
        )
        self.maxDiff = None
        self.__baseurl = 'https://baseurl.com/v2.1'
        self.__id = 1
        self.__curveRangeOutput = PagedResultCurveRangeEntity(1,2,1,False,[CurveRangeEntity(self.__id)])
        self.__curveRangeSerializedOutput = artesianJsonSerialize(self.__curveRangeOutput)
        
        return super().setUp()

    async def test_registerMarketData(self):
        expectedJson={
            'MarketDataId': 0,
            'ProviderName':"PROVIDER",
            'MarketDataName':"MARKETDATA",
            'OriginalGranularity':"Day",
            'Type':"ActualTimeSerie",
            'OriginalTimezone':"CET",
            'Tags': [{
                'Key': "PythonTag",
                'Value': ["PythonTagValue1", "PythonTagValue2"]
            }],
            'AggregationRule':"Undefined"
        }
        
        with responses.RequestsMock() as rsps:
            rsps.add('POST', self.__baseurl + '/marketdata/entity', 
                match=[responses.matchers.json_params_matcher(expectedJson)],
                json=self.__serializedOutput, status=200)

            output = await self.__service.registerMarketDataAsync(self.__sampleInput)

            self.assertEqual(output, self.__sampleOutput)
    
    async def test_readMarketDataRegistryByNameAsync(self):
        with responses.RequestsMock() as rsps:
            params = {'provider': "PROVIDER", 'curveName': "MARKETDATA"}
            rsps.add('GET', self.__baseurl + '/marketdata/entity', 
                     match=[responses.matchers.query_param_matcher(params)], 
                     json=self.__serializedOutput, status = 200)                
            output = await self.__service.readMarketDataRegistryByNameAsync(params['provider'], params['curveName'])           
            self.assertEqual(output, self.__sampleOutput)

    async def test_deleteMarketDataAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add('DELETE', self.__baseurl + '/marketdata/entity/' + str(self.__id), status=204)
            await self.__service.deleteMarketDataAsync(self.__id)
            self.assertEqual(len(rsps.calls),1)

    async def test_updateMarketDataAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add('PUT', self.__baseurl + '/marketdata/entity/'+ str(self.__id),
                json=self.__serializedOutput, status=200)
            output = await self.__service.updateMarketDataAsync(self.__id, self.__sampleInput)
            self.assertEqual(output, self.__sampleOutput)
            
    async def test_readMarketDataRegistryByIdAsync(self):
        with responses.RequestsMock() as rsps:
            rsps.add('GET', self.__baseurl + '/marketdata/entity/' + str(self.__id),
                json=self.__serializedOutput, status=200)
            output = await self.__service.readMarketDataRegistryByIdAsync(self.__id)
            self.assertEqual(output, self.__sampleOutput)

    async def test_readCurveRangePaginationAsync(self):
        with responses.RequestsMock() as rsps:
            params = {'page': '1', 'pageSize': '2'}
            rsps.add('GET', self.__baseurl + '/marketdata/entity/' + str(self.__id) + "/curves", 
                match=[responses.matchers.query_param_matcher(params)], 
                json=self.__curveRangeSerializedOutput, status = 200)            
            output = await self.__service.readCurveRangeAsync(self.__id, int(params['page']), int(params['pageSize']))       
            self.assertEqual(output, self.__curveRangeOutput)

    async def test_readCurveRangeProductAsync(self):
        with responses.RequestsMock() as rsps:
            params = {'page': '1', 'pageSize': '2', 'product': 'PRODUCT'}
            rsps.add('GET', self.__baseurl + '/marketdata/entity/' + str(self.__id) + "/curves", 
                match=[responses.matchers.query_param_matcher(params)], 
                json=self.__curveRangeSerializedOutput, status = 200)           
            output = await self.__service.readCurveRangeAsync(self.__id, int(params['page']), int(params['pageSize']), params['product'])     
            self.assertEqual(output, self.__curveRangeOutput)
    
    async def test_readCurveRangeVersionFromToAsync(self):
        with responses.RequestsMock() as rsps:
            params = {'page': '1', 'pageSize': '2','versionFrom': "2021-03-12T14:30:00", 'versionTo': "2021-03-16T14:30:00"}
            rsps.add('GET', self.__baseurl + '/marketdata/entity/' + str(self.__id) + "/curves", 
                match=[responses.matchers.query_param_matcher(params)], 
                json=self.__curveRangeSerializedOutput, status = 200)         
            output = await self.__service.readCurveRangeAsync(self.__id, int(params['page']), int(params['pageSize']), None, params['versionFrom'], params['versionTo'])        
            self.assertEqual(output, self.__curveRangeOutput)
    