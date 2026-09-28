from __future__ import annotations

import platform
from email.message import Message
from typing import Self

import msgspec
import requests

from Artesian.Exceptions import (
    ArtesianSdkForbiddenException,
    ArtesianSdkOptimisticConcurrencyException,
    ArtesianSdkRequestException,
    ArtesianSdkServerException,
    ArtesianSdkValidationException,
)

from .. import __version__
from .ArtesianJsonSerializer import artesianJsonDecode, artesianJsonEncode


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

    def __enter__(self: Self) -> Self:
        self.__session.__enter__()
        return self

    def __exit__(self: _Client, *args: object) -> None:
        self.__session.__exit__(args)

    async def exec(
        self: _Client,
        method: str,
        url: str,
        obj: object = None,
        retcls: type | None = None,
        params: dict | None = None,
    ) -> object:
        body = None if obj is None else artesianJsonEncode(obj)
        headers = None if body is None else {"Content-Type": "application/json"}
        url = self.__baseUrl + url
        r = requests.Request(method, url, data=body, headers=headers, params=params)
        prep = self.__session.prepare_request(r)
        try:
            res = self.__session.send(prep)
        except Exception as e:
            raise ArtesianSdkRequestException(f"Unexpected error while calling {method}|{url}") from e

        # Replaced the deprecated 'cgi' module (removed in Python 3.13) with 'email.message'.
        msg = Message()
        msg["content-type"] = res.headers.get("Content-Type", "")
        mimetype = msg.get_content_type()  # es. "text/html"
        _ = msg.get_params()

        if res.status_code >= 200 and res.status_code < 300:
            if mimetype == "application/json":
                return artesianJsonDecode(res.content, retcls)
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
            try:
                decoded = artesianJsonDecode(res.content)
            except msgspec.DecodeError:
                decoded = None
            if isinstance(decoded, dict):
                problemDetails = decoded
        if problemDetails is None and (
            mimetype in ("application/json", "application/problem+json") or mimetype.split("/")[0] == "text"
        ):
            errorText = res.text if res.text != "" else None

        if res.status_code == 400:  # BadRequest
            raise ArtesianSdkValidationException(method, url, res.status_code, problemDetails, errorText)
        if res.status_code in [409, 412]:  # Conflict, PreconditionFailed
            raise ArtesianSdkOptimisticConcurrencyException(method, url, res.status_code, problemDetails, errorText)
        if res.status_code in [401, 403]:  # Unauthenticated, Forbidden
            raise ArtesianSdkForbiddenException(method, url, res.status_code, problemDetails, errorText)

        # if we reached here it means that is a 500 or another unknown error
        raise ArtesianSdkServerException(method, url, res.status_code, problemDetails, errorText)
