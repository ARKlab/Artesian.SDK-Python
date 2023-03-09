from __future__ import annotations
import cgi
from typing import Any, Optional
import requests
import platform

from .ArtesianJsonSerializer import artesianJsonSerialize, artesianJsonDeserialize
from .. import __version__
from Artesian.Exceptions import (
    ArtesianSdkRequestException,
    ArtesianSdkServerException,
    ArtesianSdkValidationException,
    ArtesianSdkForbiddenException,
    ArtesianSdkOptimisticConcurrencyException,
)


class _Client:
    def __init__(self: _Client, baseUrl: str, apiKey: str) -> None:
        sdkVersion = __version__

        artesianAgentString = (
            "'ArtesianSDK-Python:"
            + sdkVersion
            + ","
            + platform.system()
            + " "
            + platform.release()
            + ":"
            + platform.version()
            + ",Python:"
            + platform.python_version()
        )
        self.__baseUrl = baseUrl
        self.__session = requests.Session()
        self.__session.headers.update(
            {
                "x-api-key": apiKey,
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Artesian-Agent": artesianAgentString,
            }
        )

    def __enter__(self: _Client) -> _Client:
        self.__session.__enter__()
        return self

    def __exit__(self: _Client, *args: Any) -> None:
        self.__session.__exit__(args)

    async def exec(
        self: _Client,
        method: str,
        url: str,
        obj: object = None,
        retcls: Optional[type] = None,
        params: Optional[dict] = None,
    ) -> Any | None:
        json = artesianJsonSerialize(obj)
        url = self.__baseUrl + url
        r = requests.Request(method, url, json=json, params=params)
        prep = self.__session.prepare_request(r)
        try:
            res = self.__session.send(prep)
        except Exception as e:
            raise ArtesianSdkRequestException(
                "Unexpected error while calling {}|{}".format(method, url)
            ) from e

        mimetype, _ = cgi.parse_header(res.headers.get("Content-Type", ""))

        if res.status_code >= 200 and res.status_code < 300:
            if mimetype == "application/json":
                return (
                    artesianJsonDeserialize(res.json(), retcls)
                    if retcls is not None
                    else res.json()
                )
            if mimetype.split("/")[0] == "text":
                return res.text
            return res.content

        # /upsertData is supposed to returns 204 thus None which would
        # not be distingushable from 404 None
        if res.status_code == 404 and retcls is not None:
            return None

        problemDetails = None
        errorText = None

        if mimetype == "application/problem+json":
            problemDetails = dict(res.json())
        if mimetype == "application/json" or mimetype.split("/")[0] == "text":
            errorText = res.text if res.text != "" else None

        if res.status_code == 400:  # BadRequest
            raise ArtesianSdkValidationException(
                method, url, res.status_code, problemDetails, errorText
            )
        if res.status_code in [409, 412]:  # Conflict, PreconditionFailed
            raise ArtesianSdkOptimisticConcurrencyException(
                method, url, res.status_code, problemDetails, errorText
            )
        if res.status_code in [401, 403]:  # Unauthenticated, Forbidden
            raise ArtesianSdkForbiddenException(
                method, url, res.status_code, problemDetails, errorText
            )

        # if we reached here it means that is a 500 or another unknown error
        raise ArtesianSdkServerException(
            method, url, res.status_code, problemDetails, errorText
        )
