import requests
import pkg_resources  # part of setuptools
import platform

class _Client:
    def __init__(self, baseUrl, apiKey):
        sdkVersion = pkg_resources.require("artesian-sdk")[0].version
        artesianAgentString = "artesian-sdk:" + sdkVersion + ", " + platform.system() + " " + platform.release() + ":"  + platform.version() + ", Python:" + platform.python_version()
        self.__baseUrl = baseUrl
        self.__session = requests.Session()
        self.__session.headers.update({'x-api-key':apiKey, 'Accept':'application/json', 'Accept-Encoding':'gzip', 'User-Agent':'Artesian.SDK-Python/1.0', 'X-Artesian-Agent': artesianAgentString})
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
