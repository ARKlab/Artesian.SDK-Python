import cgi
import requests
import platform

from Artesian._ClientsExecutor.ArtesianJsonSerializer import artesianJsonSerialize, artesianJsonDeserialize
from Artesian._package_info import __version__
from Artesian._Services.Exceptions import (ArtesianSdkRemoteException, ArtesianSdkValidationException, ArtesianSdkForbiddenException, ArtesianSdkOptimisticConcurrencyException)
import urllib.parse

class _Client:
    def __init__(self, baseUrl, apiKey):
        sdkVersion = __version__

        artesianAgentString = "'ArtesianSDK-Python:" + sdkVersion + "," + platform.system() + " " + platform.release() + ":"  + platform.version() + ",Python:" + platform.python_version()
        self.__baseUrl = baseUrl
        self.__session = requests.Session()
        self.__session.headers.update({'x-api-key':apiKey, 'Accept':'application/json', 'Accept-Encoding':'gzip', 'X-Artesian-Agent': artesianAgentString})
    def __enter__(self):
        self.__session.__enter__()
        return self
    def __exit__(self, *args):
        self.__session.__exit__(args)
    async def exec(self, method: str, url: str, obj: object = None, retcls: type = None, params = None):
        json = artesianJsonSerialize(obj)
        if(params is not None):
            url = url + "?" + urllib.parse.urlencode(params)
        r = requests.Request(method, self.__baseUrl + url, json=json)
        prep = self.__session.prepare_request(r)
        res = self.__session.send(prep)

        mimetype, _ = cgi.parse_header(res.headers['Content-Type'])

        if res.status_code >= 200 and res.status_code < 300:
            if mimetype == 'application/json':
                return artesianJsonDeserialize(res.json(), retcls)
            if mimetype.split('/')[0] == 'text':
                return res.text
            return res.content

        if res.status_code == 404:
            return None
        
        problemDetails = None
        errorText = None

        if mimetype == 'application/problem+json':
            problemDetails = res.json()
        if mimetype == 'application/json' or mimetype.split('/')[0] == 'text':
            errorText = res.text
        
        if res.status_code == 400: # BadRequest
            raise ArtesianSdkValidationException(method, self.__baseUrl + url, res.status_code, problemDetails, errorText)        
        if res.status_code in [409, 412]: # Conflict, PreconditionFailed
            raise ArtesianSdkOptimisticConcurrencyException(method, self.__baseUrl + url, res.status_code, problemDetails, errorText)
        if res.status_code in [401, 403]: # Unauthenticated, Forbidden
            raise ArtesianSdkForbiddenException(method, self.__baseUrl + url, res.status_code, problemDetails, errorText)
        
        # if we reached here it means that is a 500 or another unknown error
        raise ArtesianSdkRemoteException(method, self.__baseUrl + url, res.status_code, problemDetails, errorText)
