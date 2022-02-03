import requests
import pkg_resources  # part of setuptools
import platform
from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize, artesianJsonDeserialize
import urllib.parse

class _Client:
    def __init__(self, baseUrl, apiKey, params):
        sdkVersion = pkg_resources.require("artesian-sdk")[0].version
        artesianAgentString = "'ArtesianSDK-Python:" + sdkVersion + "," + platform.system() + " " + platform.release() + ":"  + platform.version() + ",Python:" + platform.python_version()
        self.__baseUrl = baseUrl
        self.__session = requests.Session()
        self.__session.headers.update({'x-api-key':apiKey, 'Accept':'application/json', 'Accept-Encoding':'gzip', 'X-Artesian-Agent': artesianAgentString})
        self.__params = params
    def __enter__(self):
        self.__session.__enter__()
        return self
    def __exit__(self, *args):
        self.__session.__exit__(args)
    async def exec(self, method: str, url: str, obj: object = None, retcls: type = None, params = None):
        json = artesianJsonSerialize(obj)
        if(params is not None):
            url = url + urllib.parse.urlencode(params)
        r = requests.Request(method, self.__baseUrl + url, json=json)
        prep = self.__session.prepare_request(r)
        res = self.__session.send(prep)
        res.raise_for_status()
        ret = artesianJsonDeserialize(res.json(), retcls)


        return ret