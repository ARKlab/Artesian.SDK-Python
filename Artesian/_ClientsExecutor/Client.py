import requests
class _Client:
    def __init__(self, baseUrl, apiKey):
        self.__baseUrl = baseUrl
        self.__session = requests.Session()
        self.__session.headers.update({'x-api-key':apiKey, 'Accept':'application/json', 'Accept-Encoding':'gzip', 'User-Agent':'Artesian.SDK-Python/1.0'})
    def __enter__(self):
        self.__session.__enter__()
        return self
    def __exit__(self, *args):
        self.__session.__exit__(args)
    async def exec(self, method, url, data):
        r = requests.Request(method, self.__baseUrl + url, data=data)
        prep = self.__session.prepare_request(r)
        res = self.__session.send(prep)
        res.raise_for_status()
        return res
