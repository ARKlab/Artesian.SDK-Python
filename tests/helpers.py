from __future__ import annotations
from ast import Dict
from typing import Any, Callable
from unittest.mock import Mock, patch
import Artesian.Query._Query as _Query
import Artesian.GMEPublicOffers as _GMEPO
from urllib.parse import urlparse, unquote


class Qs:
    def __init__(self: Qs, mock: Mock) -> None:
        self._mock = mock

    def getQs(self: Qs) -> Dict[str, str]:
        return dict(
            map(
                lambda x: x.split("="),
                unquote(urlparse(self._mock.call_args.args[0][0]).query).split("&"),
            )
        )

    def getPath(self: Qs) -> str:
        return urlparse(self._mock.call_args.args[0][0]).path


class QsPO:

    def __init__(self: QsPO, mock: Mock) -> None:
        self._mock = mock

    def getQs(self: QsPO) -> Dict[str, str]:
        return dict(
            map(
                lambda x: x.split("="),
                unquote(urlparse(self._mock.call_args.args[0]).query).split("&"),
            )
        )

    def getPath(self: Qs) -> str:
        return urlparse(self._mock.call_args.args[0]).path


def TrackRequests(func: Callable) -> Callable[[Any, Qs], None]:
    @patch.object(_Query._Query, "_exec")
    def wrapper(self: Any, mock: Mock) -> None:
        func(self, Qs(mock))

    return wrapper


def TrackGMEPORequests(func: Callable) -> Callable[[Any, Qs], None]:
    @patch.object(_GMEPO.GMEPublicOfferQuery, "_exec")
    def wrapper(self: Any, mock: Mock) -> None:
        func(self, QsPO(mock))

    return wrapper
